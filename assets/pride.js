const getBuffer = require('./utils.js').getBuffer
const Jimp = require('jimp')

exports.run = (URL) => {
  return new Promise(async (resolve, reject) => {
    const avatarPromise = Jimp.read(URL)
    let brazzPromise = Jimp.read('./resources/pride/gay.png')

    Promise.all([avatarPromise, brazzPromise]).then((promises) => {
      const avatar = promises[0]
      let brazz = promises[1]
      brazz.opacity(0.35)
      brazz.resize(Jimp.AUTO, 350)
      avatar.resize(350, 350)
      avatar.composite(brazz, 0, 0)
      getBuffer(avatar, resolve, reject)
    }).catch(reject)
  })
}
