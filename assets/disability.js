const { Canvas } = require('canvas-constructor')
const fsn = require('fs-nextra')
const request = require('snekfetch')

exports.run = async (URL) => {
  return new Promise(async (resolve, reject) => {
    const userPromise = await request.get(URL)
    const templatePromise = await fsn.readFile('./resources/disability/disability.jpg')
    Promise.all([userPromise, templatePromise]).then((promises) => {
      const [user, template] = promises
      let halp = new Canvas(663, 618)
        .addImage(template, 0, 0, 663, 618)
        .addImage(user.raw, 450, 325, 175, 175)
        .toBuffer()
      resolve(halp)
    }).catch(reject)
  })
}
