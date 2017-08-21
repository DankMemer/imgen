const Jimp = require('jimp')

exports.run = async (URL) => {
	return new Promise(async (resolve, reject) => {
		const avatar = await Jimp.read(URL).catch(err => {
			reject(err)
		})
		const banner = await Jimp.read('./resources/brazzers/brazzers.png')
		avatar.resize(350, 350)
		banner.resize(Jimp.AUTO, 100)
		avatar.composite(banner, 150, 275)
		avatar.getBuffer(Jimp.MIME_PNG, async (err, buffer) => {
			if (err) {
				return console.error(err.stack)
			}
			resolve(buffer)
		})
	})
}