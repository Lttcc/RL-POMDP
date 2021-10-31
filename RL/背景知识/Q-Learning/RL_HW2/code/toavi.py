import cv2
import os

video_dir = 'performance.avi' # 视频存储路径及视频名
fps = 10 # 帧率一般选择20-30
num = 64+1 # 图片数+1，因为后面的循环是从1开始
img_size = (640,480) # 图片尺寸，若和图片本身尺寸不匹配，输出视频是空的

fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
videoWriter = cv2.VideoWriter(video_dir, fourcc, fps, img_size)

for i in range(1,num):
    im_name = 'performance'+str((i-1)*10+9)+'.png'
    frame = cv2.imread(im_name)
    videoWriter.write(frame)
    print(im_name)

videoWriter.release()
print('finish')
