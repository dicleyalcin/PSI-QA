#import sys
import numpy as np
import os
import cv2
import openslide
import lxml.etree as ET
#from io import StringIO
import matplotlib.pyplot as plt
#from glob import glob
from skimage.io import imsave, imread
#from skimage.transform import resize
#from PIL import Image
from xml_to_mask import xml_to_mask
#from collections import defaultdict
import string
#import random
#import itertools

# sys.path.append('/usr/local/lib/python2.7/site-packages')
cwd = os.getcwd() # path to SVS and XMLs
# this is a path the current directory.
#print(cwd)
workdir_input=str(input("please enter the WSI and annotation data directory name: "))
#print("you entered", workdir_input)
cwd_datadir=cwd+"/"+workdir_input
#print(cwd_datadir)

print(str(cwd+"/scatterBounds"))
isDir = os.path.isdir(str(cwd+"/scatterBounds"))
isDir2 = os.path.isdir(str(cwd+"/ROIs_raw_results"))

if isDir:
    os.system("rm -r scatterBounds")
    os.system("mkdir scatterBounds")
else:
    os.system("mkdir scatterBounds")
    

if isDir2:
    os.system("rm -r ROIs_raw_results")
    os.system("mkdir ROIs_raw_results")
else:
    os.system("mkdir ROIs_raw_results")

final_image_size = 20000 # mask the structure
size_thresh = None
extract_one_region = True # include only one structure per patch (ignoring other structures in ROI)
white_background = True # mask the structure using white or black background
WSIs_=[]
XMLs_=[]

for i in os.listdir(cwd_datadir):
    if i.endswith(".svs"):
        WSIs_.append(str(i)) # absolute paths to all WSIs
    if i.endswith(".xml"):
        XMLs_.append(str(i))

ImAnnotPairs = []
for impath in WSIs_:
    for annotpath in XMLs_:
        if str(impath.replace(".svs","")) == str(annotpath.replace(".xml","")):
            ImAnnotPairs.append([impath, annotpath])
print(ImAnnotPairs) # each item is a list of image file with its xml annotation file names

def main():
    for idx,XML in enumerate(ImAnnotPairs):
        wsimg = ImAnnotPairs[idx][0]
        #print(idx,XML,wsimg)
        
        #print("-------\n")
        #print(str(cwd+"/"+workdir_input+"/"+XML[1]))
        #print("-------\n")
        xmlpath=str(cwd+"/"+workdir_input+"/"+XML[1])

        #bounds, masks = get_annotation_bounds(XML[1],1)
        bounds, masks = get_annotation_bounds(xmlpath,1)
        #print(bounds, masks)
     
        #basename = os.path.splitext(basename)[0]
        #print(basename)
        pas_img = openslide.OpenSlide(str(cwd+"/"+workdir_input+"/"+wsimg))
        print(str(cwd+"/"+workdir_input+"/"+wsimg))
        for idxx, bound in enumerate(bounds):

            print(idxx,bound)
            if extract_one_region:
                mask = masks[idxx]
            else:
                mask=(xml_to_mask(XML,(bound[0],bound[1]), (final_image_size,final_image_size), downsample_factor=1, verbose=1))
            
            if size_thresh==None:
                PAS = pas_img.read_region((int(bound[0]),int(bound[1])), 0, (final_image_size,final_image_size))
                PAS = np.array(PAS)[:,:,0:3]
            else:
                size=np.sum(mask)
                if size >= size_thresh:
                    print("")       
            if white_background:
                for channel in range(3):
                    PAS_ = PAS[:,:,channel]
                    PAS_[mask == 0] = 255
                    PAS[:,:,channel] = PAS_                     
            imsave("ROIs_raw_results/"+wsimg.replace(".svs","") + str(idxx+1) + '.jpg', PAS)
            
def get_annotation_bounds(xml_path, annotationID=1):
#def get_annotation_bounds(xml_path):
    # parse xml and get root
    tree = ET.parse(xml_path)
    root = tree.getroot() 
    bounds = []
    masks = []
    colors = []
    
    X = []
    Y = []
    for i, child in enumerate(root): # each annotation
        letters = string.digits # for writing the output
        d = child.attrib # attributes (e.g. below
        color = d.get('Color')
        colors.append(color)
        origx = []
        origy = []
        x=[]
        y=[]
        data_of_interest = []
        for grandchild in child:
            if grandchild.tag=="S":
                height = int(np.float32(grandchild.attrib['H']))
                width = int(np.float32(grandchild.attrib['W']))
                data_of_interest.append(height) # 0
                data_of_interest.append(width) # 1
            if grandchild.tag=="P":
                corner_x=int(np.float32(grandchild.attrib['X']))
                corner_y=int(np.float32(grandchild.attrib['Y']))
                data_of_interest.append(corner_x) # 2 
                data_of_interest.append(corner_y) # 3
                origx.append(int(np.float32(grandchild.attrib['X'])))
                origy.append(int(np.float32(grandchild.attrib['Y'])))
        if (len(origx) or len(origy)) == 1:
            cx = data_of_interest[0]
            cy = data_of_interest[1]
            w = data_of_interest[3]
            h = data_of_interest[2]
            y1 = list(range(cy,cy+h))
            x1 = [cx] * len(y1) 
            y2 = y1
            x2 = [cx+w+1] * len(y2)
            x3 = list(range(cx,cx+w+1))
            y3 = [cy] * len(x3)
            x4 = x3
            y4 = [cy+h] * len(x4)
            x = x1+x2+x3+x4
            y = y1+y2+y3+y4
        else:
            x = origx
            y = origy
        print(x[0],y[0],"length",len(x),len(y))
        x_center = min(x) + ((max(x)-min(x))/2)
        y_center = min(y) + ((max(y)-min(y))/2)  
        bound_x = x_center-final_image_size/2
        bound_y = y_center-final_image_size/2
        bounds.append([bound_x,bound_y])
        points = np.stack([np.asarray(x), np.asarray(y)], axis=1)
        #print(points)
        #break
        points[:,1] = np.int32(np.round(points[:,1] - bound_y ))
        points[:,0] = np.int32(np.round(points[:,0] - bound_x ))
        mask = np.zeros([final_image_size, final_image_size], dtype=np.int8)
        #mask = np.zeros([cx, cy], dtype=np.int8)
        cv2.fillPoly(mask, [points], 1)
        masks.append(mask)
        X.append(x)
        Y.append(y)

        #fig = plt.plot(x, y, 'o', color='black')
        
        fig = plt.plot(x, y, 'o', color='#'+str(hex(int(colors[i])))[4:],markersize=1)
        #FF00FF #800080
        #plt.show()
    
        #plt.savefig('Scatter_4286578816_%s.tiff' % ''.join(random.choice(letters) for i in range(3)),dpi=300) 
        #print(xml_path)
        #print(str(cwd+"/scatterBounds/"))
        xmlpath=str(xml_path).rpartition('/')[2].replace('.xml','')
        print(xmlpath)
        plt.savefig(str(cwd+"/scatterBounds/"+xmlpath)+'%s_Scatter_%s.png' % (str(i+1),str(colors[i])),dpi=300) 
        #plt.savefig('Scatter_4294902015.tiff',dpi=300)
        print(str(colors[i]))
        plt.clf()
    #print(colors)
    #print(len(X),len(Y))
    #print(masks)
    #print(len([i[0] for i in METADATA]))
    #break
    #print(colors)
    #with open('colorLabels.txt','w') as out:
    #    out.write(str(colors)+"\n")
    return bounds, masks

if __name__ == '__main__':
    main()
