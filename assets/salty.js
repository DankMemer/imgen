const Jimp = require('jimp')
const GIFEncoder = require('gifencoder')

const options = {
  size: 256,
  frames: 8
}

exports.run = (dataURL) => {
  return new Promise(async (resolve, reject) => {
    const base = new Jimp(options.size, options.size)
    const avatarPromise = Jimp.read(dataURL)
    const saltPromise = Jimp.read('./resources/salty/salt.png')

    Promise.all([avatarPromise, saltPromise]).then((promises) => {
      const [avatar, salt] = promises
      avatar.resize(options.size, options.size)
      salt.resize(256, 256)
      salt.rotate(130)

      let frames = []
      let buffers = []
      let encoder = new GIFEncoder(options.size, options.size)
      let stream = encoder.createReadStream()
      let temp

      stream.on('data', buffer => buffers.push(buffer))
      stream.on('end', () => resolve(Buffer.concat(buffers)))

      for (let i = 0; i < options.frames; i++) {
        temp = base.clone()
        temp.composite(avatar, 0, 0)

        if (i === 0) temp.composite(salt, -165, -165)
        else temp.composite(salt, -175 + getRandomInt(-5, 5), -175 + getRandomInt(-5, 5))

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
