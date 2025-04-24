import cv2
import math
from ultralytics import YOLO

model = YOLO("yolov8m.pt")


# Dictionary mapping class names to object widths
object_data = {
    "person": {"width": 100, "real_width": 170},
    "bicycle": {"width": 150, "real_width": 190},
    "car": {"width": 200, "real_width": 400},
    "motorbike": {"width": 150, "real_width": 220},
    "aeroplane": {"width": 300, "real_width": 1500},
    "bus": {"width": 400, "real_width": 1200},
    "train": {"width": 600, "real_width": 6000},
    "truck": {"width": 400, "real_width": 2400},
    "boat": {"width": 250, "real_width": 500},
    "traffic light": {"width": 50, "real_width": 80},
    "fire hydrant": {"width": 50, "real_width": 100},
    "stop sign": {"width": 50, "real_width": 75},
    "parking meter": {"width": 20, "real_width": 50},
    "bench": {"width": 150, "real_width": 200},
    "bird": {"width": 30, "real_width": 30},
    "cat": {"width": 50, "real_width": 45},
    "dog": {"width": 70, "real_width": 60},
    "horse": {"width": 150, "real_width": 210},
    "sheep": {"width": 100, "real_width": 110},
    "cow": {"width": 200, "real_width": 220},
    "elephant": {"width": 300, "real_width": 330},
    "bear": {"width": 200, "real_width": 280},
    "zebra": {"width": 200, "real_width": 250},
    "giraffe": {"width": 300, "real_width": 600},
    "backpack": {"width": 50, "real_width": 30},
    "umbrella": {"width": 50, "real_width": 70},
    "handbag": {"width": 30, "real_width": 25},
    "tie": {"width": 50, "real_width": 35},
    "suitcase": {"width": 100, "real_width": 40},
    "frisbee": {"width": 50, "real_width": 20},
    "skis": {"width": 150, "real_width": 200},
    "snowboard": {"width": 150, "real_width": 160},
    "sports ball": {"width": 50, "real_width": 20},
    "kite": {"width": 100, "real_width": 100},
    "baseball bat": {"width": 50, "real_width": 90},
    "baseball glove": {"width": 50, "real_width": 30},
    "skateboard": {"width": 100, "real_width": 80},
    "surfboard": {"width": 150, "real_width": 220},
    "tennis racket": {"width": 50, "real_width": 70},
    "bottle": {"width": 35, "real_width": 16.75},
    "wine glass": {"width": 30, "real_width": 8},
    "cup": {"width": 30, "real_width": 9},
    "fork": {"width": 20, "real_width": 18},
    "knife": {"width": 20, "real_width": 20},
    "spoon": {"width": 20, "real_width": 17},
    "bowl": {"width": 100, "real_width": 110},
    "banana": {"width": 30, "real_width": 15},
    "apple": {"width": 30, "real_width": 8},
    "sandwich": {"width": 100, "real_width": 15},
    "orange": {"width": 30, "real_width": 8},
    "broccoli": {"width": 30, "real_width": 10},
    "carrot": {"width": 20, "real_width": 15},
    "hot dog": {"width": 50, "real_width": 10},
    "pizza": {"width": 100, "real_width": 25},
    "donut": {"width": 30, "real_width": 8},
    "cake": {"width": 100, "real_width": 10},
    "chair": {"width": 100, "real_width": 50},
    "sofa": {"width": 200, "real_width": 180},
    "pottedplant": {"width": 30, "real_width": 20},
    "bed": {"width": 200, "real_width": 200},
    "diningtable": {"width": 200, "real_width": 100},
    "toilet": {"width": 70, "real_width": 40},
    "tvmonitor": {"width": 100, "real_width": 60},
    "laptop": {"width": 50, "real_width": 35},
    "mouse": {"width": 20, "real_width": 10},
    "remote": {"width": 30, "real_width": 15},
    "keyboard": {"width": 30.75, "real_width": 2.65},
    "cell phone": {"width": 15, "real_width": 3.9},
    "microwave": {"width": 50, "real_width": 50},
    "oven": {"width": 70, "real_width": 70},
    "toaster": {"width": 40, "real_width": 40},
    "sink": {"width": 50, "real_width": 50},
    "refrigerator": {"width": 100, "real_width": 100},
    "book": {"width": 14, "real_width": 1.69},
    "clock": {"width": 30, "real_width": 20},
    "vase": {"width": 30, "real_width": 20},
    "scissors": {"width": 20, "real_width": 20},
    "teddy bear": {"width": 50, "real_width": 30},
    "hair drier": {"width": 20, "real_width": 20},
    "toothbrush": {"width": 10, "real_width": 10}
}

def find(image_path, object_to_be_found):
    # return if the object is none
    if object_to_be_found == None:
        return "Nothing to detect!"
    
    # read the image and make detection
    img = cv2.imread(image_path)
    results = model.predict(img, save=True)
    founded = False

    # Define the boundaries of the three parts
    image_width = img.shape[1]
    left_boundary = image_width // 3
    right_boundary = 2 * left_boundary

    # loop through the model results
    for r in results:
        boxes = r.boxes
        if boxes:
            for box in boxes:
                class_index = int(box.cls[0])
                class_name = model.names[class_index]
                if class_name == object_to_be_found or (class_name == "cell phone" and object_to_be_found == "phone"):
                    x1, y1, x2, y2 = box.xyxy[0]
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                    w, h = x2 - x1, y2 - y1
                    conf = math.ceil((box.conf[0] * 100)) / 100
                    
                    # Calculate distance based on object data
                    obj_width = object_data[class_name]["width"]
                    focal_length = 46
                    real_width = object_data[class_name]["real_width"]
                    apparent_width = w
                    distance = round(((((obj_width * focal_length) / apparent_width * (real_width / obj_width)) + 35)) / 30.48)

                    # Check which part the object belongs to
                    if x2 < left_boundary:
                        part = "to your left"
                    elif x1 > right_boundary:
                        part = "to your right"
                    else:
                        part = "in front of you"

                    return "The " + class_name + " is " + str(distance) + " feet " + part
            if founded == False:
                return object_to_be_found + " is not found!"
        else:
            return "Nothing To Be Found!"

def test_find():
    print(find("static/logo.png", "cat"))
