const Jimp = require('jimp')
const GIFEncoder = require('gifencoder')

const frameCount = 8

exports.run = async (URL) => {
  return new Promise(async (resolve, reject) => {
    const avatarPromise = Jimp.read(URL)
    const hornPromise = Jimp.read('./resources/dank/horn.png')
    const overlayPromise = Jimp.read('./resources/dank/red.png')
    const hitPromise = Jimp.read('./resources/dank/hit.png')
    const gunPromise = Jimp.read('./resources/dank/gun.png')
    const fazePromise = Jimp.read('./resources/dank/faze.png')

    Promise.all([avatarPromise, hornPromise, overlayPromise, hitPromise, gunPromise, fazePromise]).then((promises) => {
      const [avatar, horn, overlay, hit, gun, faze] = promises
      const horn2 = horn.clone()
      avatar.resize(320, 320)
      horn.resize(100, 100)
      horn.rotate(315)
      horn.mirror(true, false)
      horn2.mirror(true, false)
      horn2.resize(130, 130)
      horn2.rotate(350)
      horn.flip(true, false)
      overlay.opacity(0.2)
      hit.resize(40, 40)
      gun.resize(250, Jimp.AUTO)
      faze.resize(Jimp.AUTO, 40)

      let buffers = []
      let frames = []
      const encoder = new GIFEncoder(256, 256)
      let stream = encoder.createReadStream()

      stream.on('data', buffer => buffers.push(buffer))
      stream.on('end', () => resolve(Buffer.concat(buffers)))

      let base = new Jimp(256, 256)

      let temp, x, y
      for (let i = 0; i < frameCount; i++) {
        temp = base.clone()
        if (i === 0) {
          x = -20
          y = -20
        } else {
          x = -25 + getRandomInt(-2, 2)
          y = -25 + getRandomInt(-2, 2)
        }
        temp.composite(avatar, -20, -20)
        temp.composite(overlay, 0, 0)
        if (i === 0) {
          x = 175
          y = 0
        } else {
          x = 165 + getRandomInt(-8, 8)
          y = 0 + getRandomInt(-0, 12)
        }
        temp.composite(horn, x, y)
        if (i === 0) {
          x = -60
          y = 0
        } else {
          x = -50 + getRandomInt(-6, 6)
          y = 0 + getRandomInt(-2, 10)
        }
        temp.composite(horn2, x, y)
        if (i === 0) {
          x = 90
          y = 65
        } else {
          x = 110 + getRandomInt(-30, 30)
          y = 55 + getRandomInt(-30, 30)
        }
        temp.composite(hit, x, y)
        temp.composite(gun, 120, 130)
        if (i === 0) {
          x = 5
          y = 212
        } else {
          x = 12 + getRandomInt(-6, 6)
          y = 210 + getRandomInt(-2, 10)
        }
        temp.composite(faze, x, y)
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
