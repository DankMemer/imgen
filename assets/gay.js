const { getBuffer } = require('./utils.js')
const Jimp = require('jimp')

exports.run = (URL) => {
  return new Promise(async (resolve, reject) => {
    const avatarPromise = Jimp.read(URL)
    const brazzPromise = Jimp.read('./resources/pride/gay.png')

    Promise.all([avatarPromise, brazzPromise]).then((promises) => {
      const [avatar, brazzers] = promises
      brazzers.opacity(0.35)
      brazzers.resize(Jimp.AUTO, 350)
      avatar.resize(350, 350)
      avatar.composite(brazzers, 0, 0)
      getBuffer(avatar, resolve, reject)
    }).catch(reject)
  })
}
