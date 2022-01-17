# muxable/av-processing

Generating an avi stream:

```sh
ffmpeg -f lavfi -i testsrc=d=10:s=640x480:r=24,format=rgb24 -f lavfi -i sine=f=440:b=4 -shortest -f avi -vcodec rawvideo -pix_fmt rgb24 output.avi
```

Playing that output:

```sh
ffplay output.avi
```

Piping to app:

```sh
cat output.avi | python3 app.py
```

Prove the pipe works without app:

```sh
ffmpeg -f lavfi -i testsrc=d=10:s=640x480:r=24,format=rgb24 -f lavfi -i sine=f=440:b=4 -shortest -f avi -vcodec rawvideo -pix_fmt rgb24 - | ffplay -
```

Piping ffmpeg through app to ffplay:

```sh
ffmpeg -f lavfi -i testsrc=d=10:s=640x480:r=24,format=rgb24 -f lavfi -i sine=f=440:b=4 -shortest -f avi -vcodec rawvideo -pix_fmt rgb24 - | python3 app.py | ffplay -
```

Productionizing, we can use `bgr24` which is supported natively by `avi`

```sh
ffmpeg -hide_banner -f lavfi -i testsrc=s=640x480:r=24 -f lavfi -i sine=f=440:b=4 -shortest -f avi -vcodec rawvideo -pix_fmt bgr24 - | python3 app.py | ffplay -
```