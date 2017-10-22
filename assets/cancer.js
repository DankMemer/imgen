const Jimp = require('jimp')

exports.run = async (URL) => {
  return new Promise(async (resolve, reject) => {
    const avatarPromise = Jimp.read(URL)
    const bannerPromise = Jimp.read('./resources/cancer/cancer.png')

    Promise.all([avatarPromise, bannerPromise]).then((promises) => {
      const [avatar, banner] = promises
      avatar.resize(100, 100)
      banner.composite(avatar, 351, 200)
      banner.getBuffer(Jimp.MIME_PNG, async (err, buffer) => {
        if (err) {
          return console.error(err.stack)
        }
        resolve(buffer)
      })
    }).catch(reject)
  })
}
