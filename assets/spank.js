const { getBuffer, tryParse } = require('./utils.js')
const Jimp = require('jimp')

exports.run = (URL) => {
  return new Promise(async (resolve, reject) => {
    URL = tryParse(URL)
    if (!URL || URL.length < 2) { return reject(new Error('data-src must be an array of 2 strings (URLs)')) }

    const [avatar, author, spank] = await Promise.all([
      Jimp.read(URL[0]),
      Jimp.read(URL[1]),
      Jimp.read('./resources/spank/spank.jpg')
    ]).catch(reject)

    avatar.resize(120, 120)
    author.resize(140, 140)
    spank.resize(500, 500)
    spank.composite(avatar, 350, 220)
    spank.composite(author, 225, 5)
    getBuffer(spank, resolve, reject)
  })
}
