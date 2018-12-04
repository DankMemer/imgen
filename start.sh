#!/bin/bash
gunicorn -w 32 -b 127.0.0.1:65535 server:app
