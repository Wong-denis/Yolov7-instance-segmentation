import cv2 
from argparse import ArgumentParser
import os

def get_parser():
    parser = ArgumentParser(description='my description')
    parser.add_argument('--input', type=str, default="", help='image or dir of images waiting for crop')
    # parser.add_argument('--dataset', type=str, default="./Image", help='where should we get the data')
    parser.add_argument('--output', type=str, default="", help='where should the output image or images be store')
    
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
crop_ratio = 0.92

if is_dir:
    if not os.path.exists(args.output):
        os.makedirs(args.output)
    image_list, filenames = LoadImageFromDir(args.input)
    for i in range(len(image_list)):
        img = image_list[i]
        h, w, chn = img.shape
        print(f'width, height = {w},{h}')
        crop_h, crop_w =(int(crop_ratio*h), int(crop_ratio*w))
        print(crop_h,crop_w)
        start = (1-crop_ratio)/2
        start_x, start_y = (int(start*h), int(start*w))
        crop_img = img[start_x:start_x+crop_h, start_y:start_y+crop_w]
        output_file = os.path.join(args.output, filenames[i].split("/")[-1])
        cv2.imwrite(output_file, crop_img)
else: 
    if os.path.isfile(args.input):
        img = cv2.imread(args.input)
        h, w, chn = img.shape
        print(f'width, height = {w},{h}')
        crop_h, crop_w =(crop_ratio*h, crop_ratio*w)
        start = (1-crop_ratio)/2
        start_x, start_y = (start*h, start*w)
        crop_img = img[start_x:start_x+crop_h, start_y:start_y:crop_w]
        cv2.imwrite(args.output, crop_img)
    else:
        raise ValueError
