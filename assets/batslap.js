const Jimp = require('jimp')

exports.run = async (URL) => {
  return new Promise(async (resolve, reject) => {
    try {
      URL = JSON.parse(URL)
    } catch (err) {
      return Promise.reject(new Error('Unable to parse data-src: ' + err.message))
    }
    if (URL.length < 2) { return Promise.reject(new Error('data-src must be an array of 2 strings (URLs)')) }

    const [avatar, author] = await Promise.all([
      Jimp.read(URL[0]),
      Jimp.read(URL[1])
    ]).catch(reject)
    const bat = await Jimp.read('./resources/batslap/batman.jpg').catch(err => {
      console.error(err.stack)
    })

    avatar.resize(150, 150)
    author.resize(130, 130)
    bat.resize(670, 400)
    bat.composite(avatar, 390, 215)
    bat.composite(author, 240, 75)
    bat.getBuffer(Jimp.MIME_PNG, async (err, buffer) => {
      if (err) {
        return console.error(err.stack)
      }
      resolve(buffer)
    })
  })
}
