const { getBuffer, tryParse } = require('./utils.js')
const Jimp = require('jimp')

exports.run = (URL) => {
  return new Promise(async (resolve, reject) => {
    URL = tryParse(URL)
    if (!URL || URL.length < 2) { return reject(new Error('data-src must be an array of 2 strings')) }

    // const username = 'oof'
    const text = URL[1]
    const avatarPromise = Jimp.read(URL[0])
    const momPromise = Jimp.read('./resources/byemom/mom.png')
    const blankPromise = Jimp.read('./resources/byemom/blank.png')
    const fontPromise = Jimp.loadFont(Jimp.FONT_SANS_16_BLACK)
    // const smolFontPromise = Jimp.loadFont(Jimp.FONT_SANS_16_BLACK)

    Promise.all([avatarPromise, momPromise, blankPromise, fontPromise]).then(async (promises) => {
      let [avatar, mom, blank, font] = promises
      const avatar2 = avatar.clone()
      avatar.resize(70, 70)
      avatar2.resize(125, 125)
      mom.composite(avatar, 530, 15)
      mom.composite(avatar2, 70, 340)
      blank.resize(275, 200)
      // mom.print(smolFont, 150, 8, `Alright ${username} im leaving the house to run some errands see you in a bit`, 175)

      const search = blank.print(font, 0, 0, text, 275)
      search.rotate(335)

      mom.composite(search, 390, 460)
      getBuffer(mom, resolve, reject)
    }).catch(reject)
  })
}
