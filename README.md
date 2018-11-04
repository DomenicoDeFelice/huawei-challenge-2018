# Huawei's Future of Vision Challenge 2018

Detect appearance of a celebrity in a video and generate a CSV file containing two columns: second of the video, `1` if the celebrity appears in that second or `0` otherwise.

**Team #2**: Global Vision

## Pipeline
1) Extract frames from video using `ffmpeg`. See `split_frames.sh`. 
2) Collect a picture of the celebrity or person you want to identify.
3) Start the face recognition classification. It uses **face recognition** by Adam Geitgey ([github](https://github.com/ageitgey/face_recognition), [pip](https://pypi.org/project/face_recognition/)), based on the state-of-the-art face recognition library [dlib](http://dlib.net/).
4) From the classification, generate the output csv file by running **generate_csv.py**. 

**Server.py** can be used two ways: when run as a script, it reads the classifications of the frames and generate a csv file (the updated part of the code that does this is in generate_csv.py). When run with Flask, it spawns a web server that has a demo application that plays the video and given the csv file, shows the seconds where the target person is recognized.
