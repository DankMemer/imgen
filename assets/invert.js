const { Canvas, invert } = require('canvas-constructor')
const request = require('snekfetch')

exports.run = async (URL) => {
  return new Promise(async (resolve, reject) => {
    const user = await request.get(URL)
      let halp = new Canvas(500, 500)
        .addImage(user.raw, 0, 0, 500, 500)
        .process(invert)
        .toBuffer()
      resolve(halp)
  })
}
