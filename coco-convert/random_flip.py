import numpy as np
import cv2
import random
import os 
from argparse import ArgumentParser

def get_parser():
    parser = ArgumentParser(description='my description')
    parser.add_argument('--input', type=str, default="", help='image or dir of images waiting for crop')
    # parser.add_argument('--dataset', type=str, default="./Image", help='where should we get the data')
    parser.add_argument('--output', type=str, default="", help='where should the output image or images be store')
    
    return parser

def random_key(len):
    key = ''
    for i in range(len):
        temp = str(random.randint(0,1))
        key += temp

    return key

def LoadImageFromDir(path):
    images = []
    filenames = []
    for filename in os.listdir(path):
        img = cv2.imread(os.path.join(path,filename))
        if img is not None:
            images.append(img)
            filenames.append(filename)
    return images,filenames

parser = get_parser()
args = parser.parse_args()
is_dir = os.path.isdir(args.input)
if is_dir:
    if not os.path.exists(args.output):
        os.makedirs(args.output)
    image_list, filenames = LoadImageFromDir(args.input)
    for i in range(len(image_list)):
        write_flag = 1
        img = image_list[i]
        h, w, chn = img.shape
        print(f'width, height = {w},{h}')
        key = random_key(2)
        if key == "00":
            flip_img = img
            write_flag = 0
        elif key == "01":
            flip_img = cv2.flip(img, 1)
        elif key == "10":
            flip_img = cv2.flip(img, 0)
        elif key == "11":
            flip_img = cv2.flip(img, -1)
        output_file = os.path.join(args.output, "flip_"+filenames[i].split("/")[-1])
        if write_flag:
            cv2.imwrite(output_file, flip_img)
else: 
    if os.path.isfile(args.input):
        img = cv2.imread(args.input)
        h, w, chn = img.shape
        print(f'width, height = {w},{h}')
        key = random_key(2)
        if key == "00":
            flip_img = img
        elif key == "01":
            flip_img = cv2.flip(img, 1)
        elif key == "10":
            flip_img = cv2.flip(img, 0)
        elif key == "11":
            flip_img = cv2.flip(img, -1)
        cv2.imwrite(args.output, flip_img)
    else:
        raise ValueError
 