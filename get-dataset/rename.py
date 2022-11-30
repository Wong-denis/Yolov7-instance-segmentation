import os
import cv2

path = "./test_dataset"
dir_list = os.listdir(path)
new_title = "wire"


for filename in dir_list:
    tail = filename.split("_")[1]
    new_filename = new_title + "_" + tail
    # print(new_filename)
    old_path = os.path.join(path, filename)
    new_path = os.path.join(path, new_filename)
    image = cv2.imread(old_path)
    cv2.imwrite(new_path, image)