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
from PIL import Image
from collections import defaultdict
import string
import random
import csv
import pandas as pd
from os import listdir
from os.path import isfile, join

cwd=os.getcwd()
#print(cwd)
# reading metadata (tsv file)
tsv_data = pd.read_csv('metadata.tsv', sep='\t')
#print(tsv_data)
#print(tsv_data["ColorTag"])
# read the filenames in scatterbounds folder
cwd_scatter=cwd+"/scatterBounds"
#print(cwd_scatter)
onlyfiles = [f for f in listdir(cwd_scatter) if isfile(join(cwd_scatter, f))]
#print(onlyfiles)
metadata=tsv_data.values.tolist()
#print(metadata)
# determine how many class labels exist in the metadata
class_labelsL = []
for entry in metadata:
	# each entry is a list 
	class_labelsL.append(entry[-1])

class_labels=list(set(class_labelsL))
groupPath = os.path.isdir(cwd+"/ROI_Groups")

if groupPath:
    os.system("rm -r ROI_Groups")
    os.system("mkdir ROI_Groups")
else:
    os.system("mkdir ROI_Groups")

for i in class_labels:
	cpath=cwd+"/ROI_Groups"+"/"+str(i)
	#print(cpath)
	if os.path.isdir(cpath):
		os.system("rm -r %s" % cpath)
		os.system("mkdir %s" % cpath)
	else:
		os.system("mkdir %s" % cpath)
#print(class_labels)

annot_trims = []
for annot in range(len(onlyfiles)):
	#print(annot)
	at = "out_"+onlyfiles[annot].split('_Scatter')[0]+".jpg"
	annot_trim = at.replace(" ", "\ ")
	#print(annot_trim)
	annot_trims.append(annot_trim)
	#break
	for entry in range(len(metadata)):
		#print(entry)
		if str(metadata[entry][0]+"-") in onlyfiles[annot]:
			if str(metadata[entry][1]+" ") in onlyfiles[annot]:
				if str("_"+str(metadata[entry][2])) in onlyfiles[annot]:
					#print(metadata[entry][3])
					#print(annot_trims[annot])		
					command = "cp %s/ROIs_raw_results_trimmed/%s %s/%s" % (cwd, str(annot_trims[annot]), cwd+"/ROI_Groups",str(metadata[entry][3]))
					print(command)
					os.system(command)
#print(annot_trims)			