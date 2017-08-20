const Jimp = require('jimp')
exports.run = (URL) => {
	return new Promise(async (resolve, reject) => {
		try {
			URL = JSON.parse(URL)
		} catch (e) {
			return reject('Unable to parse data-src.')
		}

		let fontSetting
		if (args.join(' ').length < 38) {
			fontSetting = Jimp.FONT_SANS_32_BLACK
		} else {
			fontSetting = Jimp.FONT_SANS_16_BLACK
		}

		const text = args
		const mom = await Jimp.read('./assets/imgen/ohno.png')
		const blank = await Jimp.read('./assets/imgen/Empty.png')

		mom.resize(500, 500)
		Jimp.loadFont(fontSetting).then(function (font) {
			blank.resize(250, 250)
			const search = blank.print(font, 0, 0, text, 260)

			mom.composite(search, 262, 8)
			mom.getBuffer(Jimp.MIME_PNG, async (err, buffer) => {
				await msg.channel.createMessage('', { file: buffer, name: 'ohno.png' })
			})
		})

	})
}