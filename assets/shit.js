const Jimp = require('jimp')
exports.run = (URL) => {
  return new Promise(async (resolve, reject) => {
    const text = URL
    const momPromise = Jimp.read('./resources/shit/shit.jpg')
    const blankPromise = Jimp.read('./resources/shit/Empty.png')

    Promise.all([momPromise, blankPromise]).then(async (promises) => {
      const [mom, blank] = promises
      blank.resize(350, 350)
      let font = await Jimp.loadFont(Jimp.FONT_SANS_32_BLACK)
      const search = blank.print(font, 0, 0, text, 178)
      search.rotate(310)

      mom.composite(search, 195, 585)
      mom.getBuffer(Jimp.MIME_PNG, async (err, buffer) => {
        if (err) { return reject(err.stack) }
        resolve(buffer)
      })
    }).catch(reject)
  })
}
