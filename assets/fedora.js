const { Canvas } = require('canvas-constructor')
const fsn = require('fs-nextra')
const request = require('snekfetch')

exports.run = async (URL) => {
  return new Promise(async (resolve, reject) => {
    //URL = URL.replace('.png', '.jpg')
    const userPromise = await request.get(URL)
    const templatePromise = await fsn.readFile('./resources/fedora/fedora.png')
    Promise.all([userPromise, templatePromise]).then((promises) => {
      const [user, template] = promises
      let halp = new Canvas(479, 455)
        .addImage(user.raw, 112, 101, 275, 275)
        .addImage(template, 0, 0, 479, 455)
        // .addImage(user.raw, 120, 55, 175, 175)
        .toBuffer()
      resolve(halp)
    }).catch(reject)
  })
}
