from __future__ import annotations
from configparser import Interpolation
from unicodedata import category
import numpy as np
import cv2
import json
# from os import walk
import glob
from argparse import ArgumentParser
import os 

# command example
# python3 main.py --dataset dataset512_1123 --output_file output_512_1123.json 
def get_parser():
    parser = ArgumentParser(description='my description')
    parser.add_argument('--template_file', type=str, default="annot_template_coco.json", help='coco format template')
    parser.add_argument('--dataset', type=str, default="./Image", help='where should we get the data')
    parser.add_argument('--output_file', type=str, default="output.json", help='where should the coco file be')
    parser.add_argument('--max_num', type=int, default=2, help='maximum possible number of contours')
    parser.add_argument('--min_area', type=int, default=5000, help='minimum possible area of contour')

    return parser

parser = get_parser()
args = parser.parse_args()
coco_template_path = os.path.join('./coco_json', args.template_file)
# img_path = "./Image/FLIR0169_1.png"
img_dir = args.dataset
output_file = args.output_file
out_split = output_file.split("/")
if len(out_split) == 1:
    output_file = output_file + ".json"
elif len(out_split) > 2:
    output_file = out_split[-1]

if output_file.split(".")[-1] != "json":
    output_file = output_file.split(".")[0]+".json"
output_file = "coco_json/" + output_file
possible_num_cnt = args.max_num
min_area = args.min_area

def label_contours(img_name):
    # Turn RGB image into gray then binary 
    binary_threshold = 50
    img = cv2.imread(img_name)
    # blur = cv2.blur(img, (9, 9))
    print(img_name)
    # try to transfer image to Lab color and extract L
    # lab_img = cv2.cvtColor(blur, cv2.COLOR_BGR2LAB)
    # ret, thresh = cv2.threshold(lab_img[:,:,0].reshape((img.shape[0],img.shape[1])), binary_threshold, 255, 0)
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur_gray = cv2.GaussianBlur(gray_img, (3, 3), 0)

    # blur_img = cv2.GaussianBlur(gray_img, (7, 7), 0)
    canny = cv2.Canny(blur_gray, 180, 280)
    blur_can = cv2.GaussianBlur(canny, (5, 5), 0)
    # if (blur_can>100).any():
    #     print("++++++++++++++++++++++++++++++++++++++++")
    #     print(np.array(np.nonzero(blur_can[blur_can>100])).shape)
    cv2.imshow("blur_can",blur_can)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    # os._exit()
    # blur_img = blur_img - blur_can*0.08
    # blur_img[blur_img < 1] = 1.0
    gray_img = gray_img - blur_can*0.16
    gray_img[gray_img < 0] = 0
    blur_img = cv2.GaussianBlur(gray_img, (7, 7), 0)
    blur_img = blur_img.astype(np.uint8)
    print(blur_img.shape)
    ret, thresh = cv2.threshold(blur_img, binary_threshold, 255, cv2.THRESH_BINARY_INV)
    print(thresh.shape)
    
    # h,w = thresh.shape
    # thresh[:2,:],thresh[h-2:,:],thresh[:,:2],thresh[:,w-2:] = (255,255,255,255)
    
    # Find contours in binary image
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    print(type(contours))
    contours_list = []
    for i in range(len(contours)):
        area = cv2.contourArea(contours[i])
        print(area)
        if area > min_area:
            contours_list.append(contours[i])
    contours = tuple(contours_list)
    print( "there are " + str(len(contours)) + " contours")
    cnt = contours[0]
    print ("there are " + str(len(cnt)) + " points in contours[0]")
    print(cnt[:10,:,:])
    print(hierarchy)

    # clone some images for latter adjust 
    img2 = img.copy()

    # Draw contours on the RGB image
    cv2.drawContours(img,contours,-1,(0,0,255),thickness=2,lineType=cv2.LINE_4)  # AA is better but more
    # cv2.drawContours(thresh,contours,-1,(0,0,255),thickness=4,lineType=cv2.LINE_4)  # AA is better but more
    
    # lineType: cv2.LINE_4,cv2.LINE_8(4 or 8 connected line), cv2.LINE_AA(antialiased line)
    # cv2.drawContours(img2,contours,-1,(0,255,0),thickness=3,lineType=cv2.LINE_4)  # AA is better but more

    # show images
    
    cv2.imshow('img', img)
    # cv2.imshow('img', contours)
    cv2.waitKey(0)
    # cv2.imshow("img for 4 line", img2)
    # cv2.waitKey(0)
    cv2.destroyAllWindows()
    if not os.path.exists("mask_img"):
        os.makedirs("mask_img")
    
    cv2.imwrite(os.path.join("mask_img",img_name.split("/")[-1]),img)

    # return image with contours and contours
    return img, contours

def save_to_coco(COCO_FILE_PATH, list_img_paths, list_cnts, output_file):
    file = open(COCO_FILE_PATH)
    
    # returns JSON object as seg
    data = json.load(file)

    ### images and annotation ###
    data["images"] = []
    data["annotations"] = []
    count_annot = 0
    # Iterating through the json
    # list
    list_len = len(list_img_paths)
    for i in range(list_len):
        img = cv2.imread(list_img_paths[i])
        h, w = img.shape[:2]
        # dict attributes
        attr_of_img_i = {}
        attr_of_img_i["id"] = i
        attr_of_img_i["license"] = 1
        attr_of_img_i["file_name"] = list_img_paths[i].split("/")[-1]
        attr_of_img_i["height"] = h
        attr_of_img_i["width"] = w
        # data_captured

        data['images'].append(attr_of_img_i)
        # contours shape = [#points, 1, #coordinates]
        for j in range(len(list_cnts[i])):
            attr_annot_i = {}
            attr_annot_i["id"] = count_annot
            attr_annot_i["image_id"] = i
            attr_annot_i["category_id"] = 1
            
            # segmentation and bbox 
            segmentation = []
            cnt = list_cnts[i][j]
            max_x = cnt[0,0,0]
            min_x = cnt[0,0,0]
            max_y = cnt[0,0,1]
            min_y = cnt[0,0,1]
            for k in range(cnt.shape[0]):
                x = cnt[k,0,0]
                y = cnt[k,0,1]
                segmentation.append(float(x))
                segmentation.append(float(y))
                if max_x < x : max_x = x 
                if min_x > x : min_x = x
                if max_y < y : max_y = y
                if min_y > y : min_y = y
            attr_annot_i["segmentation"] = [segmentation]
            attr_annot_i["bbox"] = [float(min_x),float(min_y),float(max_x),float(max_y)]

            attr_annot_i["iscrowd"] = 0
            attr_annot_i["area"] = int(max_x - min_x) * int(max_y - min_y)
            
            data["annotations"].append(attr_annot_i)
            count_annot +=1

        ### categories ###
        attr_cate_0 = {"id": 0, "name": "wire", "supercategory": "none"}
        attr_cate_1 = {"id": 1, "name": "wire", "supercategory": "wire"}
        data["categories"] = [attr_cate_0, attr_cate_1]
        
        
    # Serializing json
    json_object = json.dumps(data, indent=5)
    
    # Writing to sample.json
    with open(output_file, "w") as outfile:
        outfile.write(json_object)
    
    # Closing file
    file.close()

list_cnts = []
list_imgs = glob.glob(img_dir+"/*.png")
for img_path in list_imgs:
    img_label,cnt = label_contours(img_path)
    if len(cnt) <= possible_num_cnt:
        # list_cnts.append(cnt)
        pass
    list_cnts.append(cnt)
    # else:
    #     list_cnts.append(None)
# img_label, cnt = label_contours(img_path)
print("finish find contours")
print(len(list_cnts[0]))
# save_to_coco(coco_template_path, [img_path], [cnt])
save_to_coco(coco_template_path, list_imgs, list_cnts, output_file)
print("finish save coco file")

# im = cv2.imread('FLIR0169_2.png')
# imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
# ret,thresh = cv2.threshold(imgray,50,255,0)
# contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
# print( "there are " + str(len(contours)) + " contours")

# cnt = contours[0]
# print ("there are " + str(len(cnt)) + " points in contours[0]")
# print (cnt[:10])

# print(f"shape: {im.shape}")
# cv2.drawContours(im,contours,-1,(0,0,255),3,lineType=cv2.LINE_AA)
# # img = cv2.resize(im,dsize=(int(im.shape[1]*1.6),int(im.shape[0]*1.6)),interpolation=cv2.INTER_CUBIC)

# # print(img[0,:])
# cv2.imshow('im', im)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
# cv2.imwrite(img=im,filename="FLIR0169_2_o50.png")
