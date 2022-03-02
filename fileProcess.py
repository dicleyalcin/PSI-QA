import os
import itertools
from pathlib import Path
import platform
from subprocess import call
from shutil import copyfile

#print(platform.system())

cwd = os.getcwd() # path to SVS and XMLs
#print(cwd)
workdir_input=str(input("please enter the WSI and annotation data directory name: "))
cwd_datadir=str(Path(cwd+"/"+workdir_input))
#print(cwd_datadir)
cwd_datadirUX=cwd_datadir.replace(" ","\ ")
#print(cwd_datadirUX)
ldir = os.listdir(cwd_datadir)
ldir.sort()
#print(ldir)

svslist=ldir[:len(ldir)//2]
xmllist=ldir[len(ldir)//2:]


svslistlower = []
for i in svslist:
	svslistlower.append(i.lower())

#print(svslistlower)


for i in range(len(svslistlower)):
	svs=str(svslistlower[i].split('.')[0])
	svs_original=svslist[i].split('.')[0]
	xmlp=xmllist[i].split('.')[0]
	
	if svs==xmlp:
		#print(workdir_input)
		newxmlp=str(xmlp+".svs.dsmeta")
		newxmlpUX=newxmlp.replace(" ","\ ")
		towrite=str(svs_original)
		towriteUX=towrite.replace(" ","\ ")
		#print(towriteUX)
		if platform.system()=='Windows':
			#print("here")
			wpmeta=str(str(Path(str("/"+workdir_input+"/"+xmlp+".svs.dsmeta"))))
			wpmeta2=(cwd+wpmeta)
			#print(str(Path(str(svs_original+".xml"))))
			os.chdir(wpmeta2)
			wpmeta3=str(Path(cwd+wpmeta+"/notes"))
			cdest = str(Path(str(cwd_datadir+"/"+svs_original+".xml")))
			#os.system("copy %s %s" % (str("'"+wpmeta3+"'"),str("'"+cdest+"'")))				
			copyfile("{0}".format(wpmeta3), "{0}".format(cdest))	
		else:
			print("here")
			os.system("cd %s && cp notes %s" % (str(Path(str(cwd_datadirUX+"/"+newxmlpUX))), str(towriteUX+".xml")))
			os.system("cp %s %s" % (str(Path(str(cwd_datadirUX+"/"+newxmlpUX+"/"+towriteUX+".xml"))), workdir_input))		

# internally merge metadata and color_dictionary

import pandas as pd
md = pd.read_csv('metadata.tsv', sep='\t')
cd = pd.read_csv('color_dictionary.tsv',sep='\t')

merged = pd.merge(md, cd, on='ColorTag', how='left')
#print(merged)
# write the dataframe to new tsv file
merged.to_csv("metasource.tsv", sep="\t")
