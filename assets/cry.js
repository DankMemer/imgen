const { Canvas } = require('canvas-constructor')
const fsn = require('fs-nextra')

exports.run = async (URL) => {
  return new Promise(async (resolve, reject) => {
    const text = URL.replace(/\n/g, '\r\n')
    const template = await fsn.readFile('./resources/cry/cry.jpg')
    let halp = new Canvas(626, 768)
      .addImage(template, 0, 0, 626, 768)
      .setTextFont('20px Tahoma')
      .addMultilineText(text, 382, 100, 180, 21)
      .toBuffer()
    resolve(halp)
  })
}
