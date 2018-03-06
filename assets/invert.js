const { getBuffer } = require('./utils.js')
const Jimp = require('jimp')

exports.run = (URL) => {
  return new Promise(async (resolve, reject) => {
    const avatar = await Jimp.read(URL).catch(err => reject(err))
    avatar.invert()
    getBuffer(avatar, resolve, reject)
  })
}
