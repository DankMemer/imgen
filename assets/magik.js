const gm = require('gm').subClass({
  imageMagick: true
})
const sf = require('snekfetch')

exports.run = (dataURL) => {
  return new Promise(async (resolve, reject) => {
    let data = await sf.get(dataURL).catch(err => reject(err))
    if (data.status !== 200) { return reject(data.status) }
    gm(data.body).out('-liquid-rescale', '180%', '-liquid-rescale', '60%').toBuffer('PNG', (err, buffer) => {
      if (err) { return reject(err) }
      resolve(buffer)
    })
  })
}
