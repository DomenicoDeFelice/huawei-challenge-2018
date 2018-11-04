# Extract frames in JPEG format from the video. The -r option determines the number of frames per second
ffmpeg -i ../../video2.mp4 -r 2 %04d.jpg
# Optional: downsample frames to a lower resolution for better performance of the classification model
ffmpeg -i video2frames/%04d.jpg -vf scale=720x480 video2framesdownsample/%04d.jpg
