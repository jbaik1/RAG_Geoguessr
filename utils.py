import glob
import random

def get_random_image():
   """Return a dict of path image with its corresponding full country name
   args:
      None
   
   returns:
      dict with fields "country" and "image_path"
   """
   
   paths = glob.glob("./images/*/*.jpg")
   image_path = random.choice(paths)
   # ex. ./images/SLV/img_13.799272601660983,-89.23095180626325.jpg
   substr = image_path[9:]
   country_name = substr[:substr.find('/')]
   
   return {"country": country_name, "image_path": image_path}
   