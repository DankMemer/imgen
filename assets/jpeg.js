const Jimp = require('jimp')

exports.run = (URL) => {
	return new Promise(async (resolve, reject) => {
		const avatar = await Jimp.read(URL).catch(err => {
			reject(err)
		})
		avatar.pixelate(12)
		avatar.getBuffer(Jimp.MIME_PNG, async (err, buffer) => {
			if (err)
				return reject(err)
			resolve(buffer)
		})
	})
}