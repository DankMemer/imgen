const cluster = require('cluster')
const express = require('express')
const app = express()
const hb = require('handlebars')
const fs = require('fs')
const totalMem = require('os')
const freeMem = os.totalmem()

const source = hb.compile(fs.readFileSync('./index.html').toString())

const endpoints = {}
let stats = {
  apiRequests: 0,
  memUsage: 0,
  apiCmds: {}
}

fs.readdir(`${__dirname}/assets/`, async (err, files) => {
  if (err) {
    return console.error(err)
  }

  files.forEach(file => {
    file = file.replace('.js', '')
    try {
      endpoints[file] = require(`./assets/${file}`).run
      stats.apiCmds[file] = 0
    } catch (e) {
      console.warn(`There was an error with '${file}': ${e.message} | ${e.stack}`)
    }
  })
})

app.use(express.static('images'))

app.get('/stats', async (req, res) => {
  await fetchStats()
  return res.json(stats)
})

app.get('/', (req, res) => {
  process.send({dataRequest: cluster.worker.id})
  process.once('message', (message) => {
    if (message.data) {
      res.status(200).send(source(message.data))
    }
  })
})

app.get('/api/*', async (req, res) => {
  process.send('request')

  const endsWithSlash = req.originalUrl[req.originalUrl.length - 1] === '/'
  const trimmedUrl = endsWithSlash ? req.originalUrl.slice(0, -1) : req.originalUrl
  const endpoint = trimmedUrl.slice(trimmedUrl.lastIndexOf('/') + 1)

  if (!endpoints[endpoint]) {
    return res.send({ status: 404, error: `Invalid Endpoint: The requested endpoint "${endpoint}" was not found` })
  }

  const keys = require('./keys.json')
  delete require.cache[require.resolve('./keys.json')]

  if (!req.headers['api-key'] || !keys.includes(req.headers['api-key'])) {
    return res.send({ status: 401, error: 'Unauthorized: You are not authorized to access this endpoint' })
  }

  if (!req.headers['data-src']) {
    return res.send({ status: 400, error: 'Missing data-src: The required header "data-src" is missing' })
  }

  stats.apiCmds[endpoint]++
  stats.apiRequests++
  process.send({ endpoint })
  try {
    const file = await endpoints[endpoint](decodeURIComponent(req.headers['data-src']))
    res.send({ status: 200, file }) // Status is always present. Check for 200
  } catch (err) {
    console.error(`Error in endpoint '${endpoint}'`, err)
    return res.send({ status: 500, error: `${err.message}` })
  }
})

app.use(function (req, res, next) {
  res.status(404).send({error: '404: You in the wrong part of town, boi.'})
})

function launchServer () {
  const http = require('http')
  http.createServer(app).listen(80)
  console.log(`Server started on port 80 pid: ${process.pid}`)
}

if (cluster.isMaster) {
  const workerNumber = cpusLength - 1
  console.log(`Starting ${workerNumber} workers`)
  for (let i = 0; i < workerNumber; i++) {
    cluster.fork()
  }
  for (const id in cluster.workers) {
    cluster.workers[id].on('message', masterHandleMessage)
  }
} else {
  // worker
  launchServer()
}

cluster.on('online', (worker) => {
  console.log(`Worker ${worker.id} started`)
})

async function masterHandleMessage (message) {
  if (message === 'request') {
    stats.apiRequests++
  } else if (message.endpoint) {
    stats.apiCmds[message.endpoint]++
  } else if (message.dataRequest) {
    let data = {
      'uptime': formatTime(process.uptime()),
      'ram': (process.memoryUsage().rss / 1024 / 1024).toFixed(2),
      'requests': stats.apiRequests,
      'usage': Object.keys(stats.apiCmds).sort((a, b) => stats.apiCmds[b] - stats.apiCmds[a]).map(c => `${c} - ${stats.apiCmds[c]} hits`).join('<br>')
    }
    cluster.workers[message.dataRequest].send({data: data})
  }
}

function formatTime (time) {
  let days = Math.floor(time % 31536000 / 86400)
  let hours = Math.floor(time % 31536000 % 86400 / 3600)
  let minutes = Math.floor(time % 31536000 % 86400 % 3600 / 60)
  let seconds = Math.round(time % 31536000 % 86400 % 3600 % 60)
  days = days > 9 ? days : '0' + days
  hours = hours > 9 ? hours : '0' + hours
  minutes = minutes > 9 ? minutes : '0' + minutes
  seconds = seconds > 9 ? seconds : '0' + seconds
  return `${days > 0 ? `${days}:` : ``}${(hours || days) > 0 ? `${hours}:` : ``}${minutes}:${seconds}`
}

async function fetchStats () {
  let freeMem = os.freemem()
  stats.memUsage = (totalMem / 1024 / 1024) - (freeMem / 1024 / 1024)
}
