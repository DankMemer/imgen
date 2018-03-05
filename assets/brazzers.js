const { getBuffer } = require('./utils.js')
const Jimp = require('jimp')

exports.run = async (URL) => {
  return new Promise(async (resolve, reject) => {
    const avatarPromise = Jimp.read(URL)
    const bannerPromise = Jimp.read('./resources/brazzers/brazzers.png')

    Promise.all([avatarPromise, bannerPromise]).then((promises) => {
      const [avatar, banner] = promises
      avatar.resize(350, 350)
      banner.resize(Jimp.AUTO, 100)
      avatar.composite(banner, 150, 275)
      getBuffer(avatar, resolve, reject)
    }).catch(reject)
  })
}
