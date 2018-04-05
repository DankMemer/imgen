const { Canvas } = require('canvas-constructor')
const fsn = require('fs-nextra')
const request = require('snekfetch')

exports.run = async (URL) => {
  return new Promise(async (resolve, reject) => {
    const userPromise = await request.get(URL)
    const templatePromise = await fsn.readFile('./resources/door/door.jpg')
    Promise.all([userPromise, templatePromise]).then((promises) => {
      const [user, template] = promises
      let halp = new Canvas(1000, 479)
        .addImage(user.raw, 250, 0, 479, 479)
        .addImage(template, 0, 0, 1000, 479)
        // .addImage(user.raw, 512, 360, 115, 115)
        .toBuffer()
      resolve(halp)
    }).catch(reject)
  })
}
