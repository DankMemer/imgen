const { getBuffer } = require('./utils.js')
const Jimp = require('jimp')

exports.run = async (URL) => {
  return new Promise(async (resolve, reject) => {
    const avatarPromise = Jimp.read(URL)
    const bannerPromise = Jimp.read('./resources/hitler/hitler.jpeg')

    Promise.all([avatarPromise, bannerPromise]).then((promises) => {
      const [avatar, banner] = promises
      avatar.resize(140, 140)
      banner.composite(avatar, 46, 43)
      getBuffer(banner, resolve, reject)
    }).catch(reject)
  })
}
