const Jimp = require('jimp')
exports.run = (URL) => {
  return new Promise(async (resolve, reject) => {
    let args = URL
    let fontSetting
    if (args.join(' ').length < 38) {
      fontSetting = Jimp.FONT_SANS_32_BLACK
    } else {
      fontSetting = Jimp.FONT_SANS_16_BLACK
    }

    const text = args
    const momPromise = Jimp.read('./resources/ohno/ohno.png')
    const blankPromise = Jimp.read('./resources/ohno/Empty.png')

    Promise.all([momPromise, blankPromise]).then(async (promises) => {
      const [mom, blank] = promises
      mom.resize(500, 500)
      let font = await Jimp.loadFont(fontSetting)
      blank.resize(250, 250)
      const search = blank.print(font, 0, 0, text, 260)

      mom.composite(search, 262, 8)
      mom.getBuffer(Jimp.MIME_PNG, async (err, buffer) => {
        if (err) { return reject(err.stack) }
        resolve(buffer)
      })
    }).catch(reject)
  })
}
