const getBuffer = require('./utils.js').getBuffer
const Jimp = require('jimp')

exports.run = (URL) => {
  return new Promise(async (resolve, reject) => {
    const avatar = await Jimp.read(URL).catch(err => {
      console.error(err.stack)
    })
    avatar.invert()
    getBuffer(avatar, resolve, reject)
  })
}
