const { getBuffer } = require('./utils.js')
const Jimp = require('jimp')

exports.run = (URL) => {
  return new Promise(async (resolve, reject) => {
    const text = URL
    const momPromise = Jimp.read('./resources/shit/shit.jpg')
    const blankPromise = Jimp.read('./resources/shit/Empty.png')
    const fontPromise = Jimp.loadFont(Jimp.FONT_SANS_32_BLACK)

    Promise.all([momPromise, blankPromise, fontPromise]).then(async (promises) => {
      const [mom, blank, font] = promises
      blank.resize(350, 350)
      const search = blank.print(font, 0, 0, text, 178)
      search.rotate(310)

      mom.composite(search, 195, 585)
      getBuffer(mom, resolve, reject)
    }).catch(reject)
  })
}
