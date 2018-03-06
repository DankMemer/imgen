const { getBuffer, tryParse } = require('./utils.js')
const Jimp = require('jimp')

exports.run = async (URL) => {
  return new Promise(async (resolve, reject) => {
    URL = tryParse(URL)
    if (!URL || URL.length < 2) { return reject(new Error('data-src must be an array of 2 strings (URLs)')) }

    const [avatar, author, batman] = await Promise.all([
      Jimp.read(URL[0]),
      Jimp.read(URL[1]),
      Jimp.read('./resources/batslap/batman.jpg')
    ]).catch(reject)

    avatar.resize(150, 150)
    author.resize(130, 130)
    batman.resize(670, 400)
    batman.composite(avatar, 390, 215)
    batman.composite(author, 240, 75)
    getBuffer(batman, resolve, reject)
  })
}
