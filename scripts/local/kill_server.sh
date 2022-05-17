#!/bin/bash
# kill django running on port 8000
lsof -t -i tcp:8000 | xargs kill -9
# kill celery
kill -9 $(ps aux | grep celery | grep -v grep | awk '{print $2}' | tr '\n' ' ') > /dev/null 2>&1



