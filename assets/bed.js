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
        fsn.readFile('./resources/bed/bed.png')
      ])
      let halp = new Canvas(316, 768)
        .addImage(template, 0, 0, 316, 768)
        .addImage(author.raw, 25, 100, 100, 100)
        .addImage(author.raw, 25, 300, 100, 100)
        .addImage(author.raw, 53, 450, 70, 70)
        .addImage(user.raw, 53, 575, 70, 70)
        .toBuffer()
      resolve(halp)
    } catch (err) {
      console.log(err)
    }
  })
}
