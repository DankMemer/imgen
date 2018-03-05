const { getBuffer } = require('./utils.js')
const Jimp = require('jimp')

exports.run = (URL) => {
  return new Promise(async (resolve, reject) => {
    const avatarPromise = Jimp.read(URL)
    const jailPromise = Jimp.read('./resources/jail/jail.png')

    Promise.all([avatarPromise, jailPromise]).then((promises) => {
      const [avatar, jail] = promises
      avatar.resize(350, 350)
      jail.resize(350, 350)
      avatar.greyscale()
      avatar.composite(jail, 0, 0)
      getBuffer(avatar, resolve, reject)
    }).catch(reject)
  })
}
