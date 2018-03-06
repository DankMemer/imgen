const Jimp = require('jimp')

exports.run = async (URL) => {
  return new Promise(async (resolve, reject) => {
    const avatarPromise = Jimp.read(URL)
    const bannerPromise = Jimp.read('./resources/disability/disability.jpg')

    Promise.all([avatarPromise, bannerPromise]).then((promises) => {
      const [avatar, banner] = promises
      avatar.resize(175, 175)
      banner.composite(avatar, 450, 330)
      banner.getBuffer(Jimp.MIME_PNG, async (err, buffer) => {
        if (err) {
          return console.error(err.stack)
        }
        resolve(buffer)
      })
    }).catch(reject)
  })
}
