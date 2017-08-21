const Jimp = require('jimp')

exports.run = (URL) => {
	return new Promise(async (resolve, reject) => {
		const avatar = await Jimp.read(URL).catch(err => {
			console.error(err.stack)
		})
		avatar.invert()
		avatar.getBuffer(Jimp.MIME_PNG, (err, buffer) => {
			if (err)
				{return reject(err)}
			resolve(buffer)
		})
	})
}