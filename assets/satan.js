const { Canvas } = require('canvas-constructor')
const fsn = require('fs-nextra')
const request = require('snekfetch')

exports.run = async (URL) => {
  return new Promise(async (resolve, reject) => {
    const userPromise = await request.get(URL)
    const templatePromise = await fsn.readFile('./resources/satan/satan.png')
    Promise.all([userPromise, templatePromise]).then((promises) => {
      const [user, template] = promises
      let halp = new Canvas(600, 450)
        .addImage(user.raw, 200, 90, 195, 195)
        .addImage(template, 0, 0, 600, 450)
        .toBuffer()
      resolve(halp)
    }).catch(reject)
  })
}
