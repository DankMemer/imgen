#!/bin/bash
gunicorn -w 24 -b 127.0.0.1:65535 -k gevent server:app
