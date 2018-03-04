const tryParse = require('./utils.js').tryParse
const Jimp = require('jimp')

exports.run = (URL) => {
  return new Promise(async (resolve, reject) => {
    URL = tryParse(URL)
    if (!URL || URL.length < 2) { return reject(new Error('data-src must be an array of 2 strings')) }

    const text = URL[1]
    const avatarPromise = Jimp.read(URL[0])
    const momPromise = Jimp.read('./resources/byemom/mom.png')
    const blankPromise = Jimp.read('./resources/byemom/blank.png')

    Promise.all([avatarPromise, momPromise, blankPromise]).then(async (promises) => {
      let [avatar, mom, blank] = promises
      const avatar2 = avatar.clone()
      avatar.resize(70, 70)
      avatar2.resize(125, 125)
      mom.composite(avatar, 530, 15)
      mom.composite(avatar2, 70, 340)

      let font = await Jimp.loadFont(Jimp.FONT_SANS_16_BLACK)
      blank.resize(275, 200)
      let search = await blank.print(font, 0, 0, text, 275)
      search.rotate(335)

      mom.composite(search, 390, 460)
      mom.getBuffer(Jimp.MIME_PNG, async (err, buffer) => {
        if (err) { return console.error(err.stack) }
        resolve(buffer)
      })
    }).catch(reject)
  })
}
