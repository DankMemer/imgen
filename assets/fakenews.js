const { Canvas } = require('canvas-constructor')
const fsn = require('fs-nextra')
const request = require('snekfetch')

exports.run = async (URL) => {
  return new Promise(async (resolve, reject) => {
    const userPromise = await request.get(URL)
    const templatePromise = await fsn.readFile('./resources/fakenews/fakenews.png')
    Promise.all([userPromise, templatePromise]).then((promises) => {
      const [user, template] = promises
      let halp = new Canvas(763, 500)
        .addImage(user.raw, 222, 0, 300, 300)
        .addImage(template, 0, 0, 763, 500)
        .toBuffer()
      resolve(halp)
    }).catch(reject)
  })
}
