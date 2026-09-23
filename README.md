# imgen

Image generation service for Dank Memer.

The API reference, parameters, response types, and limits are listed at [memer.tech/documentation](https://memer.tech/documentation).

The service requires `config.json`, RethinkDB, Redis, and the packages in `requirements.txt`. The Linux `start.sh` script also requires Gunicorn and binds to `127.0.0.1:65535`.
