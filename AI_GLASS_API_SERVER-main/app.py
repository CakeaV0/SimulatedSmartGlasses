# ---------------------------------------
# Import Libraries ----------------------
# ---------------------------------------
import os
import shutil
import numpy as np
from ultralytics import YOLO
from waitress import serve
from datetime import datetime
from werkzeug.utils import secure_filename
from flask import Flask, request, render_template, jsonify
from finder_and_depth_estimation import find, test_find
from detection_function import *
from describe_function_2 import generate_caption_from_image, test_describe
from ocr_function import ocr_image_to_text, test_ocr
from summarize_function import summarize_text, test_summarize

# ---------------------------------------
# Define a Flask app --------------------
# ---------------------------------------
app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
model = YOLO("yolov8m.pt")

# ---------------------------------------
# Test The Program Functions ------------
# running each function to make sure that it works fine
# ---------------------------------------
print("Testing the Description Mode ............")
test_describe()
print("Done ✔️")
print("Testing the Ocr Text Mode ............")
test_ocr()
print("Done ✔️")
print("Testing the Summarize Text Mode ............")
test_summarize()
print("Done ✔️")
print("Testing the Finder Mode ............")
test_find()
print("Done ✔️")
print("Testing the Detection Mode ............")
test_detection()
print("Done ✔️")
print("---------------------------------------------------")
print("The Program Is Ready ✔️ ---------------------------")
print("---------------------------------------------------")


# ---------------------------------------
# Helper functions ----------------------
# 3shan lma na5od sora byt3mlha save bl taree5 elly it3mlha save beh 3shan fl check 3leh
# ---------------------------------------
def save_file(file):
    # create folder with name of the day
    today_date = datetime.now().strftime('%Y-%m-%d')
    today_folder_path = os.path.join(UPLOAD_FOLDER, today_date)
    if not os.path.exists(today_folder_path):
        os.makedirs(today_folder_path)
    
    # Remove folders with names other than today's date
    for folder in os.listdir(UPLOAD_FOLDER):
        folder_path = os.path.join(UPLOAD_FOLDER, folder)
        if os.path.isdir(folder_path) and folder != today_date:
            shutil.rmtree(folder_path)

    # Save the image with the current datetime
    filename = secure_filename(file.filename)
    filename = datetime.now().strftime('%Y-%m-%d_%H-%M-%S_') + filename
    file_path = os.path.join(today_folder_path, filename)
    file.save(file_path)
    return today_folder_path+'/'+filename



# ---------------------------------------
# The Main Route For Web ----------------
# ---------------------------------------
@app.route('/', methods=['GET'])
def index():
    # Main page
    names = model.names
    return render_template('index.html', names=names)


# ---------------------------------------
# The Detection Route -------------------
# ---------------------------------------
@app.route('/detect', methods=['POST'])
def detect():
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify([{
                'result': 'Something Went Wrong!',
                'mode' : 'object'
            }])
        
        selected_option = request.form.get('select_mode')
        object_to_be_found = request.form.get('object_to_be_found')
        if(selected_option == "find"):
            print("Processing ............ Mode = ", selected_option, "OTBF = ", object_to_be_found)
        else:
            print("Processing ............ Mode = ", selected_option )

        # Get the file from post request
        f = request.files['file']

        # Call save image function 
        file_path = save_file(f)

        # Make prediction
        result = None
        if(selected_option == "currency"):
            result = image_detection(file_path, "currency")
        elif(selected_option == "describe"):
            result = generate_caption_from_image(file_path)
        elif(selected_option == "text"):
            result = ocr_image_to_text(file_path)
        elif(selected_option == "text_ar"):
            result = ocr_image_to_text(file_path, lang="ar")
        elif(selected_option == "summarize"):
            result = summarize_text(file_path)
        elif(selected_option == "find"):
            result = find(file_path, object_to_be_found)
        elif(selected_option == "object"):
            result = image_detection(file_path, "object")

        print(result)
        print("Response Sent Successfully\n")
        return jsonify([
            {
                'result' : result,
                'mode' : selected_option
            }
        ])
    return None



# ---------------------------------------
# Run The App ---------------------------
# ---------------------------------------
if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=5001, threads=100)

