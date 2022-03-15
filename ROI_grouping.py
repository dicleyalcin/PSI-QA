import shutil
import sys
import numpy as np
import os
import cv2
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
from pathlib import Path
import platform
import subprocess, shlex
from shutil import copyfile


cwd=os.getcwd()
#print(cwd)
# reading metadata (tsv file)
tsv_data = pd.read_csv('metadata.tsv', sep='\t')
# reading metasource (tsv file)
tsv_data_ms = pd.read_csv('metasource.tsv', sep='\t')
#print(tsv_data)
#print(tsv_data_ms)
#print(tsv_data["ColorTag"])
# read the filenames in scatterbounds folder
cwd_scatter=cwd+"/scatterBounds"
#print(cwd_scatter)
onlyfiles = [f for f in listdir(cwd_scatter) if isfile(join(cwd_scatter, f))]
#print(onlyfiles)
metadata=tsv_data.values.tolist()
#print(metadata)
metasource=tsv_data_ms.values.tolist()
#print(metasource)

# determine how many class labels exist in the metadata
class_labelsL = []
for entry in metadata:
	# each entry is a list 
	class_labelsL.append(entry[-1])

class_labels=list(set(class_labelsL))
groupPath = os.path.isdir(cwd+"/ROI_Groups")

#print(class_labels)

if groupPath:
    os.system("rm -r ROI_Groups")
    os.system("mkdir ROI_Groups")
else:
    os.system("mkdir ROI_Groups")

# for each patient create a directory
# first get patient list


patients=[]
for m in metadata:
	patients.append(m[0])

#print(patients)
unique_patients=list(set(patients))


for p in unique_patients:
	ppath=Path(cwd+"/ROI_Groups"+"/"+p)
	#print(ppath)
	os.system("mkdir %s" % ppath)
	#break
	for i in class_labels:
		cpath=Path(cwd+"/ROI_Groups"+"/"+p+"/"+str(i))
		#print(cpath)
		#break
		if os.path.isdir(cpath):
			os.system("rm -r %s" % cpath)
			os.system("mkdir %s" % cpath)
		else:
			os.system("mkdir %s" % cpath)
	#print(class_labels)


	#print(onlyfiles)

	annot_trims = []
	for annot in range(len(onlyfiles)):
		#print(annot)
		at = str(Path("out_"+onlyfiles[annot].split('_Scatter')[0]+".jpg"))
		#print(at)
		#break
		#annot_trim = at.replace(" ", "\ ")
		#print(annot_trim)
		annot_trims.append(at)
		#break
		for entry in range(len(metadata)):
			#print(metadata[entry])
			#break
			dat = str(metadata[entry][0]+"-")
			#print(dat)
			#print(onlyfiles[annot])
			#break
			if dat in onlyfiles[annot]:
				#print("here")
				#break
				dat2 = str(metadata[entry][1]+" ")
				#print(dat2)
				#break
				if dat2 in onlyfiles[annot]:
					#print("here")
					#break
					#dat3 =str("_"+str(metadata[entry][2]))
					dat32 = str("_"+str(metasource[entry][6]))
					#print(dat3)
					#print(onlyfiles[annot])
					#break
					#print(dat32)
					#break
					if dat32 in onlyfiles[annot]:
						#print("here")
						dat_class=str(metasource[entry][5])
						#print(dat_class)
						#break
						#print(metadata[entry][3])
						#print(annot_trims[annot])
						U = Path(str(annot_trims[annot].replace(' ', "\ ")))
						#W = Path(str(annot_trims[annot].replace(' ', "` ")))
						W = Path(str(annot_trims[annot]))
						if platform.system()=='Windows':
							#command = "copy %s\ROIs_raw_results_trimmed\%s %s\%s" % (cwd, W, cwd + "\ROI_Groups", str(metasource[entry][5]))
							#print(command)
							wpmeta3 = str(Path(cwd + "\ROIs_raw_results_trimmed" + '\\' + str(W)))
							#print(wpmeta3)
							cdest = str(Path(cwd + '\ROI_Groups\\' + p + '\\' + str(metasource[entry][5])))
							#print(cdest)
							shutil.copy("{0}".format(wpmeta3), "{0}".format(cdest))
						else:
							command = "cp %s/ROIs_raw_results_trimmed/%s %s/%s/%s/" % (cwd, U, cwd+"/ROI_Groups",p,str(metasource[entry][5]))
							os.system(command)
						#print(command)
						#break
						#os.system(command)
	#print(annot_trims)
