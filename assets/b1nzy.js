const { getBuffer } = require('./utils.js')
const Jimp = require('jimp')

exports.run = (text) => {
  return new Promise(async (resolve, reject) => {
    const fontPromise = Jimp.loadFont(Jimp.FONT_SANS_16_WHITE)
    const messagePromise = Jimp.read('./resources/b1nzy/b1nzy.png')

    Promise.all([fontPromise, messagePromise]).then(resolved => {
      const [font, message] = resolved
      message.print(font, 80, 40, text, 450)
      getBuffer(message, resolve, reject)
    }).catch(err => reject(err))
  })
}
