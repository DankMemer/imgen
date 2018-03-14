const { getBuffer } = require('./utils.js')
const Jimp = require('jimp')

exports.run = (text) => {
  return new Promise(async (resolve, reject) => {
    const fontPromise = Jimp.loadFont(Jimp.FONT_SANS_32_BLACK)
    const messagePromise = Jimp.read('./resources/facts/facts.jpg')

    Promise.all([fontPromise, messagePromise]).then(resolved => {
      const [font, message] = resolved
      message.print(font, 45, 600, text, 312)
      getBuffer(message, resolve, reject)
    }).catch(err => reject(err))
  })
}
