const { getBuffer } = require('./utils.js')
const Jimp = require('jimp')

exports.run = (text) => {
  return new Promise(async (resolve, reject) => {
    const fontPromise = Jimp.loadFont(Jimp.FONT_SANS_16_BLACK)
    const messagePromise = Jimp.read('./resources/plan/plan.png')

    Promise.all([fontPromise, messagePromise]).then(resolved => {
      const [font, message] = resolved

      let words = text.split(', ')
      let a, b, c
      if (words.length < 3) {
        [a, b, c] = ['you need three items for this command', 'and each should be split by commas', 'Example: pls plan 1, 2, 3']
      } else {
        [a, b, c] = words
      }
      message.print(font, 190, 60, a, 140)
      message.print(font, 510, 60, b, 140)
      message.print(font, 190, 280, c, 140)
      message.print(font, 510, 280, c, 140)
      getBuffer(message, resolve, reject)
    }).catch(err => reject(err))
  })
}
