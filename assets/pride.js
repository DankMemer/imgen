import {getBuffer} from 'util.js'
const Jimp = require('jimp')

exports.run = (URL) => {
  return new Promise(async (resolve, reject) => {
    const avatar = await Jimp.read(URL).catch(err => {
      reject(err)
    })
    let brazz = await Jimp.read('./resources/pride/gay.png')
    brazz.opacity(0.35)
    brazz.resize(Jimp.AUTO, 350)
    avatar.resize(350, 350)
    avatar.composite(brazz, 0, 0)
    getBuffer(avatar, resolve, reject)
  })
}
