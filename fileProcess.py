import os
import itertools
from pathlib import Path
import platform
from subprocess import call
from shutil import copyfile

#print(platform.system())

cwd = os.getcwd() # path to SVS and XMLs
print(cwd)
workdir_input=str(input("please enter the WSI and annotation data directory name: "))
cwd_datadir=str(Path(cwd+"/"+workdir_input))
cwd_datadirUX=cwd_datadir.replace(" ","\ ")
#print(cwd_datadir)
ldir = os.listdir(cwd_datadir)
for i in range(len(ldir)):	
	if (i%2)==0:
		svs=ldir[i].split('.')[0].lower()
		svs_original=ldir[i].split('.')[0]
		xmlp=ldir[i+1].split('.')[0]
		if svs==xmlp:
			#print(workdir_input)
			newxmlp=str(xmlp+".svs.dsmeta")
			newxmlpUX=newxmlp.replace(" ","\ ")
			towrite=str(svs_original)
			towriteUX=towrite.replace(" ","\ ")
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
				os.system("cd %s && cp notes %s" % (str(Path(str(cwd_datadirUX+"/"+newxmlpUX))), str(towriteUX+".xml")))
				os.system("cp %s %s" % (str(Path(str(cwd_datadirUX+"/"+newxmlpUX+"/"+towriteUX+".xml"))), workdir_input))		
