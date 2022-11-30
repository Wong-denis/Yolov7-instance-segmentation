import cv2 
from argparse import ArgumentParser
import os
import numpy as np

# scale_percent = 69
resize_w = 512
resize_h = 512

def get_parser():
    parser = ArgumentParser(description='my description')
    parser.add_argument('--input', type=str, default="annot_template_coco.json", help='coco format template')
    # parser.add_argument('--dataset', type=str, default="./Image", help='where should we get the data')
    parser.add_argument('--output', type=str, default="output.json", help='where should the coco file be')
    
    return parser

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
        img = image_list[i]
        dim = (resize_w,resize_h)
        resize_img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
        # h, w, chn = img.shape
        # print(f'width, height = {w},{h}')
        # crop_h, crop_w =(int(0.84*h), int(0.84*w))
        # print(crop_h,crop_w)
        # start_x, start_y = (int(0.08*h), int(0.08*w))
        # crop_img = img[start_x:start_x+crop_h, start_y:start_y+crop_w]
        output_file = os.path.join(args.output, filenames[i].split("/")[-1])
        cv2.imwrite(output_file, resize_img)
else: 
    if os.path.isfile(args.input):
        img = cv2.imread(args.input)
        dim = (resize_w,resize_h)
        resize_img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
        # h, w, chn = img.shape
        # print(f'width, height = {w},{h}')
        # crop_h, crop_w =(0.84*h, 0.84*w)
        # start_x, start_y = (0.08*h, 0.08*w)
        # crop_img = img[start_x:start_x+crop_h, start_y:start_y:crop_w]
        cv2.imwrite(args.output, resize_img)
    else:
        raise ValueError


