const { getBuffer } = require('./utils.js')
const Jimp = require('jimp')

exports.run = (URL) => {
  return new Promise(async (resolve, reject) => {
    const text = URL.join(' ')
    const fontSetting = text.length < 38 ? Jimp.FONT_SANS_32_BLACK : Jimp.FONT_SANS_16_BLACK

    const momPromise = Jimp.read('./resources/ohno/ohno.png')
    const blankPromise = Jimp.read('./resources/ohno/Empty.png')
    const fontPromise = Jimp.loadFont(fontSetting)

    Promise.all([momPromise, blankPromise, fontPromise]).then(async (promises) => {
      const [mom, blank, font] = promises
      mom.resize(500, 500)
      blank.resize(250, 250)
      const search = blank.print(font, 0, 0, text, 260)
      mom.composite(search, 262, 8)
      getBuffer(mom, resolve, reject)
    }).catch(reject)
  })
}
