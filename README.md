# Huawei's Future of Vision Challenge 2018

Detect appearance of a celebrity in a video and generate a CSV file containing two columns: second of the video, `1` if the celebrity appears in that second or `0` otherwise.

**Team #2**: Global Vision

## Pipeline
1) Extract frames from video using `ffmpeg`. See `split_frames.sh`. 
2) Collect a picture of the celebrity or person you want to identify.
3) Start the face recognition classification. It uses **face recognition** by Adam Geitgey ([github](https://github.com/ageitgey/face_recognition), [pip](https://pypi.org/project/face_recognition/)), based on the state-of-the-art face recognition library [dlib](http://dlib.net/).
4) From the classification, generate the output csv file by running **generate_csv.py**. 

**Server.py** can be used two ways: when run as a script, it reads the classifications of the frames and generate a csv file (the updated part of the code that does this is in generate_csv.py).

When run with Flask, it can be used to manually check the CSV file. It spawns a web server with a demo application that plays the video and and highlights the seconds where the target person is identified.

Technologies used for the web app: JavaScript, HTML5 Canvas, [AI Projector](https://github.com/DomenicoDeFelice/ai-projector), Flask, python.

Given the size, the video is not included in this repository.

**Challenge #1: Detecting Tom Cruise**
![Challenge #1: Detecting Tom Cruise](https://domdefelice.net/wp-content/uploads/2018/11/Detecting-Tom-Cruise.png "Challenge #1: Detecting Tom Cruise")
