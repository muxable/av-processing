# syntax=docker/dockerfile:1

FROM python:3-alpine

# build dependencies for libav
RUN apk update && apk add pkgconfig ffmpeg-dev gcc musl-dev

RUN pip install av

COPY src /app

CMD ["python", "/app/main.py"]