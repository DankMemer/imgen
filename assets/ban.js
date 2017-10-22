const Jimp = require('jimp')

exports.run = async (URL) => {
  return new Promise(async (resolve, reject) => {
    const avatarPromise = Jimp.read(URL)
    const bannerPromise = Jimp.read('./resources/ban/ban.png')

    Promise.all([avatarPromise, bannerPromise]).then((promises) => {
      const [avatar, banner] = promises
      avatar.resize(350, 350)
      banner.composite(avatar, 93, 365)
      banner.getBuffer(Jimp.MIME_PNG, async (err, buffer) => {
        if (err) {
          return console.error(err.stack)
        }
        resolve(buffer)
      })
    }).catch(reject)
  })
}
