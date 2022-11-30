import cv2
from argparse import ArgumentParser


def get_parser():
    parser = ArgumentParser(description='my description')
    parser.add_argument('--video_path', type=str, help='complete path for video wanted to extract')
    parser.add_argument('--resize_ratio', type=float, default=1.0, help='ratio of the output picture, default to be 1')
    # parser.add_argument('--resize_abs', type=int, default=640, help='absolute image size you want')
    parser.add_argument('--window', type=float, default=1.0, help='window ration ')
    return parser

parser = get_parser()
args = parser.parse_args()
cam = cv2.VideoCapture(args.video_path)
# cable_video/output-2022-11-16-17-09-27.mp4

cv2.namedWindow("test")

width  = cam.get(3)  # float `width`
height = cam.get(4)  # float `height`
print(f'original: ({width},{height})')
resize_w = int(width*args.resize)
resize_h = int(height*args.resize)


img_counter = 30

while True:
    ret, frame = cam.read()
    cv2.imshow("test", cv2.resize(frame, (int(width*args.window), int(height*args.window))))
    frame = cv2.resize(frame, (resize_w,resize_h))
    if not ret:
        break
    k = cv2.waitKey(80)

    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    elif k%256 == 32:
        # SPACE pressed
        img_name = "video_dataset/cable_{}.png".format(img_counter)
        cv2.imwrite(img_name, frame)
        print("{} written!".format(img_name))
        img_counter += 1

cam.release()

cv2.destroyAllWindows()