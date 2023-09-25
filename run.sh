#!/bin/bash

dockerize -wait tcp://db:3306 -timeout 20s

# 서버 타입에 따른 명령어 실행
if [ "$SERVER_TYPE" == "HTTP" ]; then
    gunicorn main:app --workers 8 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:80
elif [ "$SERVER_TYPE" == "GRPC" ]; then
    python3 grpc-main.py
else
    echo "Unknown SERVER_TYPE: $SERVER_TYPE"
    exit 1
fi
