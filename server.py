import io
import os
import csv
import re
import random
import time
from flask import Flask, request
from flask_cors import CORS
from clarifai.rest import ClarifaiApp, Image as ClImage
from base64 import b64decode

CELEBRITY = 'tom cruise'
CLASS = 'Tom_Cruise'
THRESHOLD = 0.3
FRAMES_DIR = 'frames/'
PREDICTIONS_FILE = "OpenFaceResults_clean.txt"

#  ______ _           _       _____           _   _             
# |  ____| |         | |     / ____|         | | (_)            
# | |__  | | __ _ ___| | __ | (___   ___  ___| |_ _  ___  _ __  
# |  __| | |/ _` / __| |/ /  \___ \ / _ \/ __| __| |/ _ \| '_ \ 
# | |    | | (_| \__ \   <   ____) |  __/ (__| |_| | (_) | | | |
# |_|    |_|\__,_|___/_|\_\ |_____/ \___|\___|\__|_|\___/|_| |_|
#                                                            
# This file can be either executed on its own as a script, or as a
# Flask web application.
# This section contain the Flask code that is used to perform a demo
# relying on Clarifai.
# The actual classification is performed when running it as a script: 
# scroll down to find it.
#
clapp = ClarifaiApp(api_key='API_KEY_HERE')
model = clapp.models.get('celeb-v1.3')

app = Flask(__name__)
CORS(app)

@app.route('/predict', methods=['POST', 'GET', 'OPTIONS'])
def predict():
    if request.method != 'POST':
        return ''

    payload = request.get_json()
    base64Image = payload['image']

    p = celebrity_classifier(b64decode(base64Image), CELEBRITY)

    return "{\"%s\": %f}" % (CELEBRITY.title(), p)

def celebrity_classifier(image, celebrity):
    "Returns the probability of `celebrity` being in `image`."
    image = ClImage(file_obj=io.BytesIO(image))
    prediction = model.predict([image])

    celebrities_detected = extract_people_from_prediction(prediction)

    if celebrity not in celebrities_detected: return 0
    return celebrities_detected[celebrity]

def extract_people_from_prediction(prediction):
    "Returns a {name: probability} dict from a prediction"
    celebrities_detected = {}
    try:
        regions = prediction['outputs'][0]['data']['regions']
        for region in regions:
            celebrities_detected.update(extract_celebrities_from_region(region))
    except KeyError:
        pass

    return celebrities_detected

def extract_celebrities_from_region(region):
    "Returns a {name: probability} dict from a region"
    try:
        people = region['data']['face']['identity']['concepts']
        return dict([(person['name'], person['value']) for person in people if person['value'] >= THRESHOLD])
    except KeyError:
        return {}

#   _____              _ _      _   _                _____           _     
#  |  __ \            | (_)    | | (_)              / ____|         | |    
#  | |__) | __ ___  __| |_  ___| |_ _  ___  _ __   | (___   ___  ___| |_   
#  |  ___/ '__/ _ \/ _` | |/ __| __| |/ _ \| '_ \   \___ \ / _ \/ __| __|  
#  | |   | | |  __/ (_| | | (__| |_| | (_) | | | |  ____) |  __/ (__| |_ _ 
#  |_|   |_|  \___|\__,_|_|\___|\__|_|\___/|_| |_| |_____/ \___|\___|\__(_)
#
def gen_csv_from_predictions_file(filename):
    with open(filename, mode='rb') as file:
        predictions = file.read().splitlines()

    celebrity_predictions = [
        (
            second_from_frame_number(get_frame_number_from_prediction(prediction)),
            get_classification_from_prediction(prediction)
        )
        for prediction in predictions
    ]
    celebrity_predictions.sort()

    with open('results_%d.csv' % time.time(), 'wb') as csvfile:
        csvwriter = csv.writer(csvfile)
        last_second = None
        celebrity_in_second = False

        for second, classification in celebrity_predictions:
            if second != last_second:
                if last_second is not None:
                    print("%d , %d" % (last_second , int(celebrity_in_second)))
                    csvwriter.writerow([last_second, int(celebrity_in_second)])
                last_second = second
                celebrity_in_second = False

            celebrity_in_second = celebrity_in_second or classification == CLASS

        if last_second != None:
            print("%d , %d" % (last_second , int(celebrity_in_second)))
            csvwriter.writerow([last_second, int(celebrity_in_second)])

def get_frame_number_from_prediction(prediction):
    p = re.compile('/(\d+)\.jpg')
    match = p.search(prediction)
    return int(match.group(1))
        
def get_classification_from_prediction(prediction):
    p = re.compile(',(.+)')
    match = p.search(prediction)
    return match.group(1)

def second_from_frame_number(frame_number):
    return (frame_number - 1) // 3 + 1

#####################################################################
#####################################################################
#####################################################################

# This determines if the file is being run as a script or with Flask.
if __name__ == "__main__":
    gen_csv_from_predictions_file(PREDICTIONS_FILE)
