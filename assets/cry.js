const { getBuffer } = require('./utils.js')
const Jimp = require('jimp')

exports.run = (URL) => {
  return new Promise(async (resolve, reject) => {
    const text = URL.replace(/\n/g, '\r\n')
    const font = await Jimp.loadFont(Jimp.FONT_SANS_16_BLACK)
    const cry = await Jimp.read('./resources/cry/cry.jpg')

    cry.print(font, 377, 83, text, 210)
    getBuffer(cry, resolve, reject)
  })
}
