const Jimp = require('jimp')

async function getBuffer (avatar, resolve, reject) {
  avatar.getBuffer(Jimp.MIME_PNG, (err, buffer) => {
    if (err) { return reject(err) }
    resolve(buffer)
  })
}

async function tryParse (URL) {
  try {
    URL = JSON.parse(URL)
  } catch (err) {
    return Promise.reject(new Error('Unable to parse data-src: ' + err.message))
  }
  return URL;
}

module.exports = {
  tryParse: tryParse,
  getBuffer: getBuffer
};
