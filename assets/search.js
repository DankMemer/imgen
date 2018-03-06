const { getBuffer } = require('./utils.js')
const Jimp = require('jimp')

exports.run = (URL) => {
  return new Promise(async (resolve, reject) => {
    const text = URL
    const momPromise = Jimp.read('./resources/search/thesearch.png')
    const blankPromise = Jimp.read('./resources/search/Empty.png')
    const fontPromise = Jimp.loadFont(Jimp.FONT_SANS_16_BLACK)

    Promise.all([momPromise, blankPromise, fontPromise]).then(async (promises) => {
      const [mom, blank, font] = promises
      blank.resize(275, 200)
      blank.resize(250, 250)
      const search = blank.print(font, 0, 0, text, 178)

      mom.composite(search, 65, 335)
      getBuffer(mom, resolve, reject)
    }).catch(reject)
  })
}
