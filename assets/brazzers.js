const Jimp = require('jimp')

exports.run = (URL) => {
	return new Promise(async (resolve, reject) => {
		const avatar = await Jimp.read(URL).catch(err => {
			reject(err)
		})
		const banner = await Jimp.read('./resources/brazzers/brazzers.png')
		avatar.resize(350, 350)
		banner.resize(Jimp.AUTO, 100)
		avatar.composite(banner, 150, 275)
		avatar.getBuffer(Jimp.MIME_PNG, (err, buffer) => {
			if (err)
				return reject(err)
			resolve(buffer)
		})
	})
}