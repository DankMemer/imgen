const tryParse = require('./utils.js').tryParse
const Jimp = require('jimp')

exports.run = (URL) => {
  return new Promise(async(resolve, reject) => {
    URL = await tryParse(URL)
    if (URL.length < 2) { return Promise.reject(new Error('data-src must be an array of 2 strings')) }

    const text = URL[1].replace(/\n/g, '\r\n')
    const avatarPromise = Jimp.read(URL[0])
    const cryPromise = Jimp.read('./resources/cry/cry.jpg')

    Promise.all([avatarPromise, cryPromise]).then(async (promises) => {
      let [avatar, cry] = promises
      
      let font = await Jimp.loadFont(Jimp.FONT_SANS_16_BLACK)
      cry.print(font, 377, 83, text, 210)
  
      cry.getBuffer(Jimp.MIME_PNG, async(err, buffer) => {
        if (err) { return console.error(err.stack) }
        resolve(buffer)
      })
    }).catch(reject)
  })
}
