# ----------------------------------------------------------------
# ---------------------- Import Libraries ------------------------
# ----------------------------------------------------------------
import os
import cv2
import time
import pyttsx3
import threading
import pygame.mixer
from datetime import datetime
import speech_recognition as sr
from api_request import detect

current_directory = os.path.dirname(__file__)

# ----------------------------------------------------------------
# ----------- Function To Convert The Text Into Speech -----------
# ----------------------------------------------------------------
def speak(text):
    engine = pyttsx3.init() 
    voices = engine.getProperty('voices') 
    engine.setProperty('voice', voices[1].id) 
    engine.say(text)
    engine.runAndWait()

class AiGlassesSystem:
    def __init__(self):
        self.video_loop_active = False
        self.cap = cv2.VideoCapture(0)  # Open the default camera
        self.mixer = pygame.mixer
        self.mixer.init()
        self.system_active = True  # Flag to indicate if the system is active
        self.object_names = {'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket', 'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone', 'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush', '0.25', '0.50', '1',  '10', '100', '20', '200', '5', '50'}

    def start_system(self):
        voice_thread = threading.Thread(target=self.listen_for_commands)
        voice_thread.start()

    def listen_for_commands(self):
        recognizer = sr.Recognizer()
        microphone = sr.Microphone()
        self.speak_and_print("Hello, I am the smart glasses for blind people. I am Listening...", "AI Glasses")

        while self.system_active:
            with microphone as source:
                sound = self.mixer.Sound(os.path.join(current_directory, 'static', 'start.mp3'))
                sound.set_volume(0.3) 
                sound.play()
                recognizer.adjust_for_ambient_noise(source)
                print("AI Glasses: I am Listening...")
                audio = recognizer.listen(source, 8, 3)

            try:
                command = str(recognizer.recognize_google(audio).lower())
                print(f"You Said: {command}")
                
                if  "exit" in command :
                    self.exit()
                
                elif  "detect" in command :
                    self.capture_and_process("object")
                
                if  "money" in command :    
                    self.capture_and_process("currency")
                
                if  "describe" in command :
                    self.capture_and_process("describe")
                
                if  "read text" in command :
                    self.capture_and_process("text")
                
                elif command.startswith("find"):
                    self.handle_find(command[5:])
                
                elif  "video" in command :
                    self.start_video_loop()
                
                elif  "stop" in command :
                    self.stop_video_loop()
                
            except sr.UnknownValueError:
                print("AI Glasses: Could not understand audio, try again.")
            except sr.RequestError as e:
                print(f"AI Glasses: Error with the speech recognition service; {0}".format(e))

    def handle_find(self, text):
        words = text.split()
        filtered_words = [word for word in words if word.lower() not in ['the', 'a', 'an']]
        object_to_be_found = ' '.join(filtered_words)

        if object_to_be_found in self.object_names:
            self.capture_and_process("find", object_to_be_found)
        else:
            self.speak_and_print(f"{object_to_be_found} Is Not An Object to be found!", "AI Glasses")


    def start_video_loop(self):
        self.video_loop_active = True
        video_loop = threading.Thread(target=self.open_video_capture)
        video_loop.start()

    def stop_video_loop(self):
        self.video_loop_active = False

    def open_video_capture(self, duration=15):
        if not self.cap.isOpened():
            print("Error: Could not open camera.")
            return
        self.speak_and_print("Video mode is active for 15 seconds. Say stop to end it.", "AI Glasses")
        start_time = time.time()
        elapsed_time = 0
        while self.video_loop_active and elapsed_time < duration:
            self.capture_and_process("object")
            elapsed_time = time.time() - start_time

        self.speak_and_print("The Video Mode Is Off. i am Listening", "AI Glasses")
        self.stop_video_loop()
        cv2.destroyAllWindows()

    def capture_and_process(self, mode, object_to_be_found=None):
        self.mixer.Sound(os.path.join(current_directory, 'static', 'camera.mp3')).play()
        ret, frame = self.cap.read()

        if ret:
            # Delete all files in uploads folder
            for root, dirs, files in os.walk('static/uploads'):
                for file in files:
                    os.unlink(os.path.join(root, file))
                
                # Save the new frame in the uploads folder
                now = datetime.now() # date now
                image_filename = f"static/uploads/captured_image_{now.strftime('%Y%m%d%H%M%S')}.jpg"
                cv2.imwrite(image_filename, frame) # save image with the date to uploads file

                if mode == 'describe':
                    self.speak_and_print(f"The Describe Mode Takes Some Time, Please wait a few second!", "AI Glasses")

                # Call Detect Function to detect objects
                result = detect(image_filename, mode, object_to_be_found) # call detect method
                if result:
                    self.speak_and_print(result, "AI Glasses")
                else:
                    self.speak_and_print("Something went wrong with the server!", "AI Glasses")
        else:
            self.speak_and_print("Something went wrong with the camera!", "AI Glasses")

    def speak_and_print(self, text, channel):
        print(f"{channel}: {text}")
        speak(text)

    def exit(self):
        self.speak_and_print("Goodbye, See you soon!", "AI Glasses")
        self.stop_video_loop()
        self.system_active = False

# Example usage
ai_glasses = AiGlassesSystem()
ai_glasses.start_system()
