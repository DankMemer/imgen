const { MIME_PNG } = require('jimp')

function getBuffer (image, resolve, reject) {
  image.getBuffer(MIME_PNG, (err, buffer) => {
    if (err) { return reject(err) }
    resolve(buffer)
  })
}

function tryParse (URL) {
  try {
    return JSON.parse(URL)
  } catch (err) {
    return null
  }
}

module.exports = {
  tryParse: tryParse,
  getBuffer: getBuffer
}
