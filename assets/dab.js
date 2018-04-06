const { Canvas } = require('canvas-constructor')
const fsn = require('fs-nextra')
const request = require('snekfetch')

exports.run = async (URL) => {
  return new Promise(async (resolve, reject) => {
    // URL = URL.replace('png', 'jpg')
    const userPromise = await request.get(URL)
    const templatePromise = await fsn.readFile('./resources/dab/dab.png')
    Promise.all([userPromise, templatePromise]).then((promises) => {
      const [user, template] = promises
      let halp = new Canvas(800, 611)
        .addImage(user.raw, 300, 0, 500, 500)
        .addImage(template, 0, 0, 800, 611)
        .toBuffer()
      resolve(halp)
    }).catch(reject)
  })
}
