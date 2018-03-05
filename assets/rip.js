const { getBuffer } = require('./utils.js')
const Jimp = require('jimp')

exports.run = async (URL) => {
  return new Promise(async (resolve, reject) => {
    const avatarPromise = Jimp.read(URL)
    const bannerPromise = Jimp.read('./resources/rip/rip.png')

    Promise.all([avatarPromise, bannerPromise]).then((promises) => {
      const [avatar, banner] = promises
      avatar.resize(300, 300)
      banner.resize(642, 806)
      banner.composite(avatar, 175, 385)
      getBuffer(banner, resolve, reject)
    }).catch(reject)
  })
}
