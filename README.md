# Starting meme-server
`cd` to meme-server

run `gunicorn -w 32 -b 127.0.0.1:65535 server:app`

Change 127.0.0.1:65535 to reflect desired host and port. Run on 0.0.0.0:port to expose it to the internet
