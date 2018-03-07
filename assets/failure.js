const { getBuffer } = require('./utils.js')
const Jimp = require('jimp')

exports.run = async (URL) => {
  return new Promise(async (resolve, reject) => {
    const avatarPromise = Jimp.read(URL)
    const eggPromise = Jimp.read('./resources/failure/failure.jpg')

    Promise.all([avatarPromise, eggPromise]).then((promises) => {
      const [avatar, egg] = promises
      avatar.resize(215, 215)
      egg.composite(avatar, 143, 525)
      getBuffer(egg, resolve, reject)
    }).catch(reject)
  })
}
