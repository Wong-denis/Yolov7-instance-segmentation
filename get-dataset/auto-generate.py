import cv2
import os
import time
from threading import Timer

# channel=1 for infray
# channel=0 for rgb
vcap = cv2.VideoCapture("rtsp://192.168.0.200:554/cam/realmonitor?channel=1&subtype=0&unicast=true&proto=Onvif")
## rtsp://192.168.0.177:9554/live?channel=0&subtype=0
## rtsp://admin:148575@192.168.0.106:554/live/profile.0
## rtsp://admin:INFRACHEN123@192.168.0.17/Streaming/Channels/101
## rtsp://192.168.0.200:554/cam/realmonitor?channel=1&subtype=0&unicast=true&proto=Onvif
cv2.namedWindow("test")

width  = vcap.get(3)  # float `width`
height = vcap.get(4)  # float `height`
print(f'({width*0.6},{height*0.6})')

# # Number of frames to capture
# num_frames = 60
# print("Capturing {0} frames".format(num_frames))

# # Start time
# start = time.time()
# # Grab a few frames
# for i in range(0, num_frames):
#     ret, frame = vcap.read()
# # End time
# end = time.time()

# # Time elapsed
# seconds = end - start
# print("Time taken : {0} seconds".format(seconds))

# # 计算FPS，alculate frames per second
# fps  = num_frames / seconds
# print("Estimated frames per second : {0}".format(fps))

img_counter = 0
dirname = "./test_dataset"
print()
def show_image(vcap):
    ret, frame = vcap.read()
    resize = cv2.resize(frame, (int(width*0.6),int(height*0.6)))
    cv2.imshow("test", resize)
    return ret, resize

total = 0
ret = True
while ret:
    total += 1
    ret, resize = show_image(vcap)
    k = cv2.waitKey(1)
    
    if k%256 == 27 or total > 3600:
        # ESC pressed
        print("Escape hit, closing...")
        break
    # elif k%256 == 32:
    elif total % 180 == 0:
        # SPACE pressed
        # total = 5
        # while total>0:
        #     print("{} second left".format(total))
        #     time.sleep(1)
        #     total -= 1
        # t = Timer(5 , show_image(vcap))
        # t.start()
        img_name = "cable_{}.png".format(img_counter)
        path = os.path.join(dirname, img_name)
        cv2.imwrite(path, resize)
        print("{} written!".format(img_name))
        img_counter += 1

vcap.release()

cv2.destroyAllWindows()