const Jimp = require('jimp')

exports.run = (URL) => {
	return new Promise(async (resolve, reject) => {
		const avatar = await Jimp.read(URL).catch(err => {
			return reject(err)
		})
		const jail = await Jimp.read('./resources/jail/jail.png').catch(err => {
			return reject(err)
		})
		avatar.resize(350, 350)
		jail.resize(350, 350)
		avatar.greyscale()
		avatar.composite(jail, 0, 0)
		avatar.getBuffer(Jimp.MIME_PNG, async (err, buffer) => {
			if (err)
				return reject(err)
			resolve(buffer)
		})
	})
}