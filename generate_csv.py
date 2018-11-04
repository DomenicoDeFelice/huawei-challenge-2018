#!/usr/bin/env python

import io
import os
import csv
import re
import random
import time

# CLASS = 'Tom_Cruise'
# CLASS = 'harry'
CLASS = 'pic1'
# PREDICTIONS_FILE = "OpenFaceResults_clean.txt"
# PREDICTIONS_FILE = "harry_clean_classifications.txt"
PREDICTIONS_FILE = "mystery_person_clean_classifications.txt"
FRAMES_PER_SEC = 2

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
    return (frame_number - 1) // FRAMES_PER_SEC + 1

#####################################################################
#####################################################################
#####################################################################

# This determines if the file is being run as a script or with Flask.
if __name__ == "__main__":
    gen_csv_from_predictions_file(PREDICTIONS_FILE)
