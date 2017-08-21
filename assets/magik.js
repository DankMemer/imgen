const gm = require('gm').subClass({
	imageMagick: true
})
const sf = require('snekfetch')

exports.run = (dataURL) => {
	return new Promise(async (resolve, reject) => {
		let data = await sf.get(dataURL).catch(err => {
			return reject(err.message)
		})
		if (data.status !== 200)
			return reject(data.status)
		gm(data.body)
			.out('-liquid-rescale', '50x50%', '-resize', '500%')
			//.implode(-1)
			//.swirl(`${getRandomInt(0, 1) === 1 ? '+' : '-'}${getRandomInt(40, 80)}`)
			.toBuffer('PNG', (err, buffer) => {
				if (err)
					return reject(err)
				resolve(buffer)
			})
	})
}

function getRandomInt(min, max) {
	return Math.floor(Math.random() * (max - min + 1)) + min
}