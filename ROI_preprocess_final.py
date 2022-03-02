import sys
import numpy as np
import os
import cv2
import openslide
import lxml.etree as ET
import matplotlib.pyplot as plt
from glob import glob
from skimage.io import imsave, imread
from skimage.transform import resize
from PIL import Image, ImageChops
from collections import defaultdict
import string
import random

Image.MAX_IMAGE_PIXELS = None

def trim(im):
    bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
    diff = ImageChops.difference(im,bg)
    diff = ImageChops.add(diff,diff,2.0,-100)
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)



cwd=os.getcwd()

trimPath = cwd+"/ROIs_raw_results"
#print(trimPath)
newPath = os.path.isdir(cwd+"/ROIs_raw_results_trimmed")
#print(newPath)
newPathP=cwd+"/ROIs_raw_results_trimmed"
if newPath:
    os.system("rm -r ROIs_raw_results_trimmed")
    os.system("mkdir ROIs_raw_results_trimmed")
else:
    os.system("mkdir ROIs_raw_results_trimmed")


for j in os.listdir(trimPath):
    #a = j.replace(" ","\ ")
    #print(a)
    b = j.replace(".jpg","")
    print(b)
    #print(newPath+"/"+b)
    #print(str(trimPath+"/"+b))
    inputimage = "%s.jpg" % str(trimPath+"/"+b)
    outputimage = "%s/out_%s.jpg" % (str(newPathP), str(b))
    print(inputimage)
    print(outputimage)
    
    im = Image.open(inputimage)
    im = trim(im)
    im.save(outputimage)


