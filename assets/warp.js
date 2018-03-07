const sf = require('snekfetch')
const gm = require('gm').subClass({
  imageMagick: true
})

exports.run = (dataURL) => {
  return new Promise(async (resolve, reject) => {
    let data = await sf.get(dataURL).catch(err => reject(err))
    if (data.status !== 200) { return reject(new Error('Server returned ' + data.status)) }
    gm(data.body).implode(`-${getRandomInt(3, 15)}`).roll(`+${getRandomInt(0, 256)}+${getRandomInt(0, 256)}`).swirl(`${getRandomInt(0, 1) === 1 ? '+' : '-'}${getRandomInt(120, 180)}`).toBuffer('PNG', (err, buf) => {
      if (err) { return reject(err) }
      resolve(buf)
    })
  })
}

function getRandomInt (min, max) {
  return Math.floor(Math.random() * (max - min + 1)) + min
}
