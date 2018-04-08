const { getBuffer } = require('./utils.js')
const Jimp = require('jimp')

exports.run = (text) => {
  return new Promise(async (resolve, reject) => {
    const fontPromise = Jimp.loadFont(Jimp.FONT_SANS_32_BLACK)
    const messagePromise = Jimp.read('./resources/brain/brain.jpg')

    Promise.all([fontPromise, messagePromise]).then(resolved => {
      const [font, message] = resolved

      let words = text.split(',')
      let a, b, c, d
      if (words.length < 4) {
        [a, b, c, d] = ['you need', 'four items', 'for this', 'command (should be 3 commas)']
      } else {
        [a, b, c, d] = words
      }
      message.print(font, 15, 40, a, 225)
      message.print(font, 15, 230, b, 225)
      message.print(font, 15, 420, c, 225)
      message.print(font, 15, 610, d, 225)
      getBuffer(message, resolve, reject)
    }).catch(err => reject(err))
  })
}
