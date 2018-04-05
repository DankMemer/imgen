const { getBuffer } = require('./utils.js')
const Jimp = require('jimp')

exports.run = (text) => {
  return new Promise(async (resolve, reject) => {
    const fontPromise = Jimp.loadFont(Jimp.FONT_SANS_16_BLACK)
    const messagePromise = Jimp.read('./resources/angryman/angryman.png')

    Promise.all([fontPromise, messagePromise]).then(resolved => {
      const [font, message] = resolved
      message.print(font, 395, 480, text, 200)
      getBuffer(message, resolve, reject)
    }).catch(err => reject(err))
  })
}
