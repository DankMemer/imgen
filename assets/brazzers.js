const { Canvas } = require('canvas-constructor')
const fsn = require('fs-nextra')
const request = require('snekfetch')

exports.run = async (URL) => {
  return new Promise(async (resolve, reject) => {
    const userPromise = await request.get(URL)
    const templatePromise = await fsn.readFile('./resources/brazzers/brazzers.png')
    Promise.all([userPromise, templatePromise]).then((promises) => {
      const [user, template] = promises
      let halp = new Canvas(500, 500)
        .addImage(user.raw, 0, 0, 500, 500)
        .addImage(template, 200, 390, 300, 150)
        .toBuffer()
      resolve(halp)
    }).catch(reject)
  })
}
