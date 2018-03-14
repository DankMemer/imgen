const { getBuffer, tryParse } = require('./utils.js')
const Jimp = require('jimp')

exports.run = (URL) => {
  return new Promise(async (resolve, reject) => {
    URL = tryParse(URL)
    if (!URL || URL.length < 2) { return reject(new Error('data-src must be an array of 2 strings')) }

    const text = URL[1]
    const avatarPromise = Jimp.read(URL[0])
    const momPromise = Jimp.read('./resources/floor/floor.jpg')
    const fontPromise = Jimp.loadFont(Jimp.FONT_SANS_16_BLACK)

    Promise.all([avatarPromise, momPromise, fontPromise]).then(async (promises) => {
      let [avatar, mom, font] = promises
      const avatar2 = avatar.clone()
      avatar.resize(45, 45)
      avatar2.resize(23, 23)
      mom.composite(avatar, 100, 90)
      mom.composite(avatar2, 330, 90)
      mom.print(font, 160, 42, text, 400)
      getBuffer(mom, resolve, reject)
    }).catch(reject)
  })
}
