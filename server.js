const cluster = require('cluster')
const express = require('express')
const https = require('https')
const app = express()
const fs = require('fs')
const r = require('rethinkdbdash')()
const config = require('config.json')

const cpusLength = require('os').cpus().length
app.use('/', express.static('./static'))

const endpoints = {}
const stats = {
  requests: 0,
  cmds: {}
}

fs.readdir(`${__dirname}/assets/`, async (err, files) => {
  if (err) {
    return console.error(err)
  }

  files.forEach(file => {
    file = file.replace('.js', '')
    try {
      endpoints[file] = require(`./assets/${file}`).run
      stats.cmds[file] = 0
    } catch (e) {
      console.warn(`There was an error with '${file}': ${e.message} | ${e.stack}`)
    }
  })
})

app.use(express.static('images'))

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

  process.send({ endpoint })
  try {
    const file = await endpoints[endpoint](req.headers['data-src'])
    res.send({ status: 200, file }) // Status is always present. Check for 200
  } catch (err) {
    console.error(`Error in endpoint '${endpoint}'`, err)
    return res.send({ status: 500, error: `${err.message}` })
  }
})

//DBL webhooks
app.post('/dblwebhook', async (req, res) => {
  if(req.headers.Authorization) {
    if(req.headers.Authorization === config.webhook_secret) {
      req.body.type === 'upvote' ? await addCoins(req.body.user, 500)
      : await removeCoins(req.body.user, 500);
    }
  } 
  else {
    res.send({status: 403, error: 'Pls stop.'})
  }
})

function launchServer () {
  const http = require('http');
  http.createServer(app).listen(80);
  console.log(`Server started on port 80 pid: ${process.pid}`)
}

if (cluster.isMaster) {
  const workerNumber = cpusLength - 1
  let memoryUsageCounter = 0
  console.log(`Starting ${workerNumber} workers`)
  for (let i = 0; i < workerNumber; i++) {
    cluster.fork()
  }
  async function masterHandleMessage (message) {
    if (message === 'request') {
      stats.requests++
    } else if (message.endpoint) {
      stats.cmds[message.endpoint]++
    } else if (message.dataRequest) {
      let data = {
        'uptime': formatTime(process.uptime()),
        'ram': (process.memoryUsage().rss / 1024 / 1024).toFixed(2),
        'requests': stats.requests,
        'usage': Object.keys(stats.cmds).sort((a, b) => stats.cmds[b] - stats.cmds[a]).map(c => `${c} - ${stats.cmds[c]} hits`).join('<br>')
      }
      cluster.workers[message.dataRequest].send({data: data})
    }
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

async function addCoins (id, amount) {
  let coins = await this.getCoins(id)
  // if (coins.changes) coins = coins.changes[0].new_val
  coins.coin += amount

  return r.table('coins')
    .insert(coins, { conflict: 'update' })
}

async function removeCoins (id, amount) {
  let coins = await this.getCoins(id)
  // if (coins.changes) coins = coins.changes[0].new_val
  if (coins.coin - amount <= 0) {
    coins.coin = 0
  } else {
    coins.coin -= amount
  }

  return r.table('coins')
    .insert(coins, { conflict: 'update' })
}
