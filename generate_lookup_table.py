import csv
import os
import re

cwd = os.getcwd()
#print(cwd)
scatterBounds=os.path.join(cwd,'scatterBounds')
#print(scatterBounds)
ROIs_raw_results=os.path.join(cwd,'ROIs_raw_results')
#print(ROIs_raw_results)
metasource=os.path.join(cwd,'metasource.tsv')
#print(metasource)

listSB=[]
for i in os.listdir(scatterBounds):
    listSB.append(i)

listROIs = []
for i in os.listdir(ROIs_raw_results):
    listROIs.append(i)

#print(len(listSB))
#print(len(listROIs))


f = open(metasource)
ROIs = []
with f as fd:
    rd = csv.reader(fd,delimiter='\t',quotechar='"')
    for row in rd:
        # print([row[2],row[6]])
        ROIs.append([row[1],row[2],row[6]])

ROIs=ROIs[1:]
#print(ROIs)
#print(len(ROIs))

"""
groups = {}
for l in ROIs:
    groups.setdefault(l[0], []).append(l)

listROIs=list(groups.values())
# print(listROIs)
#print(len(listROIs))
"""

patients=[item[0] for item in ROIs]
#print(patients)


# function to get unique values
def unique(list1):
    # initialize a null list
    unique_list = []
    # traverse for all elements
    for x in list1:
        # check if exists in unique_list or not
        if x not in unique_list:
            unique_list.append(x)
    return unique_list


unique_patients=unique(patients)
#print(unique_patients)



lookup_interims = []
if len(unique_patients)==1:
    lookup_interim = []
    for i in ROIs:
        scatterlist = []
        #print(i)
        #break
        for j in listSB:
            #print(j)
            #print(str(i[0]))
            #print(str(i[1]))
            #print(str(i[2]))
            #s=str(i[1])+"\D"
            #p=re.compile(s)
            #a=p.findall(j)
            #stra=''.join(a)
            #print(stra)
            #print(p)
            if (str(i[0]) in j) and (str(i[1])+" " in j) and (str(i[2]) in j):
                scatterlist.append(j)
        lookup_interim.append(scatterlist)
    lookup_interims.append(lookup_interim)

#print(lookup_interims)
#print(len(lookup_interims))

pfinalwords=[]
for i in lookup_interims: # each patient
    finalwords=[]
    #print(i)
    #break
    patient=i[0][0]
    patient2=patient.split("-")[0]
    finalwords.append(patient2)
    for j in i: # each ROI
        finalword=[]
        if len(j)==1: # one image in the ROI
            #print("one")
            word = j[0]
            a = re.findall("A\d", word)
            b = re.findall("M\d", word)
            w = a[0] + b[0]
            #print(w)
            finalword.append(w)
        else:
            #print(j)
            #print(len(j))
            for M in j:
                word = M
                #print(word)
                a=re.findall("A\d",word)
                b=re.findall("M\d",word)
                w=a[0]+b[0]
                #print(w)
                finalword.append(w)
        #print(finalword)
        finalwords.append(finalword)

        #break
    #print(finalwords)
    pfinalwords.append(finalwords)

# print(pfinalwords)
# print(len(pfinalwords))

for i in pfinalwords:
    print(i) # this is one patient's data
    #patient 1. make a file, defining the name
    patientname = i[0] # this is a string
    f = open(patientname+"_lookup.txt","w")
    #f.write(str(patientname)+"\n")
    for j in range(1,len(i)):
        print(i[j]) # this is the first line on the lookup table.
        # processing..
        newline=','.join(i[j])
        print(newline)
        f.write(newline+"\n")




