const { getBuffer } = require('./utils.js')
const Jimp = require('jimp')

exports.run = (URL) => {
  return new Promise(async (resolve, reject) => {
    const text = URL[1].replace(/\n/g, '\r\n')
    const font = await Jimp.loadFont(Jimp.FONT_SANS_16_WHITE)
    const message = await Jimp.read('./resources/b1nzy/b1nzy.png').catch(err => reject(err))

    message.print(font, 80, 40, text, 450)
    getBuffer(message, resolve, reject)
  })
}
