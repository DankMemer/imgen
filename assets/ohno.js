const Jimp = require('jimp')
exports.run = (URL) => {
  return new Promise(async(resolve, reject) => {
    try {
      URL = JSON.parse(URL)
    } catch (err) {
      return Promise.reject(new Error('Unable to parse data-src: ' + err.stack))
    }
    let args = URL[0]
    let fontSetting
    if (args.join(' ').length < 38) {
      fontSetting = Jimp.FONT_SANS_32_BLACK
    } else {
      fontSetting = Jimp.FONT_SANS_16_BLACK
    }

    const text = args
    const mom = await Jimp.read('./resources/ohno/ohno.png')
    const blank = await Jimp.read('./resources/ohno/Empty.png')

    mom.resize(500, 500)
    let font = await Jimp.loadFont(fontSetting)
    blank.resize(250, 250)
    const search = blank.print(font, 0, 0, text, 260)

    mom.composite(search, 262, 8)
    mom.getBuffer(Jimp.MIME_PNG, async(err, buffer) => {
      if (err) { return reject(err.stack) }
      resolve(buffer)
    })
  })
}
