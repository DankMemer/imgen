const { getBuffer, tryParse } = require('./utils.js')
const Jimp = require('jimp')

exports.run = (URL) => {
  return new Promise(async (resolve, reject) => {
    URL = tryParse(URL)
    if (!URL || URL.length < 2) { return reject(new Error('data-src must be an array of 2 strings (URLs)')) }

    const [avatar, author] = await Promise.all([
      Jimp.read(URL[0]),
      Jimp.read(URL[1])
    ]).catch(reject)
    const spank = await Jimp.read('./resources/spank/spank.jpg').catch(err => {
      reject(err)
    })

    avatar.resize(120, 120)
    author.resize(140, 140)
    spank.resize(500, 500)
    spank.composite(avatar, 350, 220)
    spank.composite(author, 225, 5)
    getBuffer(spank, resolve, reject)
  })
}
