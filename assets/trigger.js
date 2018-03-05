const Jimp = require('jimp')
const GIFEncoder = require('gifencoder')

const options = {
  size: 256,
  frames: 8
}

exports.run = (dataURL) => {
  return new Promise(async (resolve, reject) => {
    let base = new Jimp(options.size, options.size)
    let avatarPromise = Jimp.read(dataURL)
    let textPromise = Jimp.read('./resources/triggered/triggered.jpg')
    let tintPromise = Jimp.read('./resources/triggered/red.png')

    Promise.all([avatarPromise, textPromise, tintPromise]).then((promises) => {
      const [avatar, text, tint] = promises
      avatar.resize(320, 320)

      let frames = []
      let buffers = []
      let encoder = new GIFEncoder(options.size, options.size)
      let stream = encoder.createReadStream()
      let temp

      stream.on('data', buffer => buffers.push(buffer))
      stream.on('end', () => resolve(Buffer.concat(buffers)))

      for (let i = 0; i < options.frames; i++) {
        temp = base.clone()

        if (i === 0) temp.composite(avatar, -16, -16)
        else temp.composite(avatar, -32 + getRandomInt(-16, 16), -32 + getRandomInt(-16, 16))

        temp.composite(tint, 0, 0)

        if (i === 0) temp.composite(text, -10, 200)
        else temp.composite(text, -12 + getRandomInt(-8, 8), 200 + getRandomInt(0, 12))

        frames.push(temp.bitmap.data)
      }

      encoder.start()
      encoder.setRepeat(0)
      encoder.setDelay(20)
      for (let frame of frames) encoder.addFrame(frame)
      encoder.finish()
    }).catch(reject)
  })
}

function getRandomInt (min, max) {
  return Math.floor(Math.random() * (max - min + 1)) + min
}
