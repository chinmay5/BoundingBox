# -*- coding: utf-8 -*-
"""
Created on Wed Dec  9 14:55:43 2015
This script is to convert the txt annotation files to appropriate format needed by YOLO 
@author: Guanghan Ning
Email: gnxr9@mail.missouri.edu
"""

import re
import os
from os import walk, getcwd
from PIL import Image

classes = [""]

def convert(size, box):
    dw = 1./size[0]
    dh = 1./size[1]
    x = (box[0] + box[1])/2.0
    y = (box[2] + box[3])/2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)
    
    
"""-------------------------------------------------------------------""" 

""" Configure Paths"""   
mypath = "./"
outpath = "./Yolo_format_output/"

cls = ""

#Image format

EXTENSION="jpg"

#if cls not in classes:
#    exit(0)
cls_id = classes.index(cls)

wd = getcwd()
list_file = open('%s/%s_list.txt'%(wd, cls), 'w')

""" Get input text file list """
txt_name_list = []
for (dirpath, dirnames, filenames) in walk(mypath):
    for filename in filenames:
        if re.match('\D*\d+.txt',filename) is not None:
             txt_name_list.append(filename)

#print("Text name list is ",txt_name_list)

""" Process """
for txt_name in txt_name_list:
    # txt_file =  open("Labels/stop_sign/001.txt", "r")
    
    """ Open input text files """
    txt_path = mypath + txt_name
    #print("Input:" + txt_path)
    txt_file = open(txt_path, "r")
    lines = txt_file.read().splitlines()   #for ubuntu, use "\r\n" instead of "\n"
    
    """ Open output text files """
    txt_outpath = outpath + txt_name
    #print("Output:" + txt_outpath)
    txt_outfile = open(txt_outpath, "w")
    
    print("Attempting conversion for ",txt_name)
    """ Convert the data to YOLO format """
    ct = 0
    for line in lines:
        #print('lenth of line is: ')
        #print(len(line))
        #print('\n')
        if(len(line) >= 2):
            ct = ct + 1
            #print(line + "\n")
            elems = line.split(' ')
            #print(elems)
            cls_id = elems[0]
            xmin = elems[1]
            xmax = elems[3]
            ymin = elems[2]
            ymax = elems[4]
            #
            img_path = str('%s/%s.%s'%(wd,  os.path.splitext(txt_name)[0], EXTENSION))
            #t = magic.from_file(img_path)
            #wh= re.search('(\d+) x (\d+)', t).groups()
            im=Image.open(img_path)
            w= int(im.size[0])
            h= int(im.size[1])
            #w = int(xmax) - int(xmin)
            #h = int(ymax) - int(ymin)
            # print(xmin)
            #print(w, h)
            b = (float(xmin), float(xmax), float(ymin), float(ymax))
            bb = convert((w,h), b)
            #print(bb)
            txt_outfile.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

    """ Save those images with bb into list"""
    if(ct != 0):
        list_file.write('%s/%s.%s'%(wd,  os.path.splitext(txt_name)[0], EXTENSION)+"\n")
                
list_file.close()