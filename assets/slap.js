const { Canvas } = require('canvas-constructor')
const fsn = require('fs-nextra')
const request = require('snekfetch')
const { tryParse } = require('./utils.js')

exports.run = async (URL) => {
  return new Promise(async (resolve, reject) => {
    URL = tryParse(URL)
    try {
      const [user, author, template] = await Promise.all([
        request.get(URL[0]),
        request.get(URL[1]),
        fsn.readFile('./resources/batslap/batman.jpg')
      ])

      let halp = new Canvas(1000, 500)
        .addImage(template, 0, 0, 1000, 500)
        .addImage(user.raw, 580, 260, 220, 220)
        .addImage(author.raw, 350, 70, 200, 200)
        .toBuffer()
      resolve(halp)
    } catch (err) {
      console.log(err)
    }
  })
}
