import glob
import random
import os

paths = glob.glob("./images/*/*.jpg")
total_num_files = len(paths)
num_files = total_num_files
print(num_files)
removed = set()

while num_files > total_num_files//10:
   path = paths[random.randint(0,total_num_files-1)]
   if path in removed:
      continue
   else:
      os.remove(path)
      removed.add(path)   
      num_files -= 1

paths = glob.glob("./images/*/*.jpg")
num_files = len(paths)
print(num_files)
