const Jimp = require('jimp')

exports.run = (URL) => {
	return new Promise(async (resolve, reject) => {
		try {
			URL = JSON.parse(URL)
		} catch (e) {
			return reject('Unable to parse data-src.')
		}
		if (URL.length < 2)
			return reject('data-src must be an array of 2 strings (URLs)')

		const [avatar, author] = await Promise.all([
			Jimp.read(URL[0]),
			Jimp.read(URL[1])
		]).catch(reject)
		const bat = await Jimp.read('./resources/batman/batman.jpg').catch(err => {
			reject(err)
		})

		avatar.resize(150, 150)
		author.resize(130, 130)
		bat.resize(670, 400)
		bat.composite(avatar, 390, 215)
		bat.composite(author, 240, 75)
		bat.getBuffer(Jimp.MIME_PNG, (err, buffer) => {
			if (err)
				return reject(err)
			resolve(buffer)
		})
	})
}