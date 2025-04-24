from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import cv2

processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")

def generate_caption_from_image(image_path):
  image = cv2.imread(image_path)
  inputs = processor(image, return_tensors="pt", max_new_tokens=100)
  out = model.generate(**inputs)
  caption = processor.decode(out[0], skip_special_tokens=True)
  return caption



def test_describe():
  print(generate_caption_from_image('static/logo.png'))