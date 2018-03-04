const Jimp = require('jimp')
exports.run = (URL) => {
  return new Promise(async (resolve, reject) => {
    const text = URL
    const momPromise = Jimp.read('./resources/search/thesearch.png')
    const blankPromise = Jimp.read('./resources/search/Empty.png')

    Promise.all([momPromise, blankPromise]).then(async (promises) => {
      const [mom, blank] = promises
      blank.resize(275, 200)
      let font = await Jimp.loadFont(Jimp.FONT_SANS_16_BLACK)
      blank.resize(250, 250)
      const search = blank.print(font, 0, 0, text, 178)

      mom.composite(search, 65, 335)
      mom.getBuffer(Jimp.MIME_PNG, async (err, buffer) => {
        if (err) { return reject(err.stack) }
        resolve(buffer)
      })
    }).catch(reject)
  })
}
