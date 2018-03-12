const { getBuffer } = require('./utils.js')
const Jimp = require('jimp')

exports.run = async (URL) => {
  return new Promise(async (resolve, reject) => {
    const avatarPromise = Jimp.read(URL)
    const bannerPromise = Jimp.read('./resources/trash/trash.png')

    Promise.all([avatarPromise, bannerPromise]).then((promises) => {
      const [avatar, banner] = promises
      avatar.resize(483, 483)
      avatar.blur(7)
      banner.composite(avatar, 480, 0)
      getBuffer(banner, resolve, reject)
    }).catch(reject)
  })
}
