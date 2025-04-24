import requests
import json


# ----------------------------------------------------------------
# ------------------- Function To Get Result ---------------------
# ----------------------------------------------------------------
def get_result(text):
  result_list = json.loads(text) # Parse the JSON string
  return result_list[0].get("result")


# ----------------------------------------------------------------
# -------------------- Function To Detect -----------------------
# ----------------------------------------------------------------
def detect(image_filename, mode, object_to_be_found=None):
  api_url = 'http://127.0.0.1:5001/detect'

  files = {'file': open(image_filename, 'rb')} # open image file
  data_payload = { 'select_mode': mode }

  if mode == 'find':
    data_payload = { 'select_mode': mode, "object_to_be_found": object_to_be_found }

  try:
    response = requests.post(api_url, data=data_payload, files=files) # send post request to detect image objects
    if response.status_code == 200:
      detections = get_result(response.text)
      return detections
    else:
      print(f"Error {response.status_code}: {response.text}")
  except:
    return None
  return None
