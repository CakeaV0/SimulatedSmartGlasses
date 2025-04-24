from txtai.pipeline import Summary
from ocr_function import ocr_image_to_text


def summarize_text(image_path):
 text = ocr_image_to_text(image_path)
 if text == "Nothing To Read":
   return "Nothing To Summarize"
 else:
  summary = Summary()
  result = summary(text)
  if result:
   return result
  else:
   return "Nothing To Summarize"



def test_summarize():
  print(summarize_text("static/logo.png"))