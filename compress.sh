#!/bin/bash

input_video="videos/unmuted/mw2019/comp_4_touro.mp4"
output_video="touro.mp4"

target_size_MB=64
duration=$(ffmpeg -i $input_video 2>&1 | grep Duration | awk '{print $2}' | tr -d ,)
hours=$(echo $duration | cut -d":" -f1)
minutes=$(echo $duration | cut -d":" -f2)
seconds=$(echo $duration | cut -d":" -f3 | cut -d"." -f1)
total_seconds=$(echo "$hours*3600+$minutes*60+$seconds" | bc)
bitrate=$(echo "($target_size_MB*8192)/$total_seconds" | bc)

ffmpeg -i $input_video -b:v ${bitrate}k -bufsize ${bitrate}k $output_video
