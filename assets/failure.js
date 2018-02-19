const Jimp = require('jimp')

exports.run = async (URL) => {
  return new Promise(async (resolve, reject) => {
    const avatarPromise = Jimp.read(URL)
    const eggPromise = Jimp.read('./resources/egg/egg.png')

    Promise.all([avatarPromise, eggPromise]).then((promises) => {
      const [avatar, egg] = promises
      egg.resize(350, 350)
      avatar.resize(Jimp.AUTO, 50)
      egg.composite(avatar, 143, 188)
      egg.getBuffer(Jimp.MIME_PNG, async (err, buffer) => {
        if (err) {
          return console.error(err.stack)
        }
        resolve(buffer)
      })
    }).catch(reject)
  })
}
