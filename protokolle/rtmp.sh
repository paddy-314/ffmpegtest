INPUT="${INPUT:-dev/source.mp4}"

ffmpeg -stream_loop -1 -re \
	-i "$INPUT" \
    -pixel_format uyvy422 \
    -c:v libx264 -preset ultrafast -tune zerolatency -crf 23 \
    -vf "drawtext=fontfile=/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf:text='sent at\:' '%{localtime\\:%X.%N}':fontcolor=white@1:box=1:boxcolor=black@1:boxborderw=8:fontsize=36:x=7:y=7" \
	-an \
    -f flv "rtmp://innolable.ddnss.de:1935/mystream"