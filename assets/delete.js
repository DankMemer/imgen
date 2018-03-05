const { getBuffer } = require('./utils.js')
const Jimp = require('jimp')

exports.run = async (URL) => {
  return new Promise(async (resolve, reject) => {
    const avatarPromise = Jimp.read(URL)
    const bannerPromise = Jimp.read('./resources/delete/delete.png')

    Promise.all([avatarPromise, bannerPromise]).then((promises) => {
      const [avatar, banner] = promises
      avatar.resize(195, 195)
      banner.composite(avatar, 120, 135)
      getBuffer(banner, resolve, reject)
    }).catch(reject)
  })
}