const { getBuffer } = require('./utils.js')
const Jimp = require('jimp')

exports.run = (URL) => {
  return new Promise(async (resolve, reject) => {
    const text = URL.replace(/\n/g, '\r\n')
    const font = await Jimp.loadFont(Jimp.FONT_SANS_64_BLACK)
    const tweet = await Jimp.read('./resources/tweet/trump2.jpg')

    tweet.print(font, 45, 160, text, 1250)
    getBuffer(tweet, resolve, reject)
  })
}
