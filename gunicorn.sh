#!/bin/bash
gunicorn -w 4 server:app
