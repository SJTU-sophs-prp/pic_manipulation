import os

import cv2
import numpy as np
from PIL import Image

Image.MAX_IMAGE_PIXELS = None
import math


def ver_cut(img_root, width, height, overlap_rate, save_root, start_point, zfill_num):
    im = Image.open(img_root)
    img_size = im.size
    m = img_size[0]  # 读取图片的宽度
    n = img_size[1]  # 读取图片的高度
    w = width
    h = height

    start_loc = int(h * (1 - overlap_rate))
    loop_num = math.ceil(n / start_loc)

    if not os.path.isdir(save_root):
        os.makedirs(save_root)

    for j in range(loop_num):
        y = start_loc * j  # 裁剪起点的y坐标范围
        region = im.crop((0, y, w, y + h))  # 裁剪区
        region.save(save_root + str(j+start_point).zfill(zfill_num) + ".jpg")
    print("finish")


def total_cut(img_root, resize, width, height, overlap_x, overlap_y, save_root, start_point, zfill_num):
    im = Image.open(img_root)
    im = im.resize(resize)
    print(resize)
    img_size = im.size
    m = img_size[0]  # 读取图片的宽度
    n = img_size[1]  # 读取图片的高度
    w = width
    h = height

    start_loc_x = int(w * (1 - overlap_x))
    start_loc_y = int(h * (1 - overlap_y))
    col = math.ceil(m / start_loc_x) - int(w / start_loc_x) + 1
    row = math.ceil(n / start_loc_y) - int(h / start_loc_y) + 1

    if not os.path.isdir(save_root):
        os.makedirs(save_root)
    count = 0
    for i in range(col):
        for j in range(row):
            x = start_loc_x * i  # 裁剪起点的x坐标范围
            y = start_loc_y * j  # 裁剪起点的y坐标范围
            region = im.crop((x, y, x + w, y + h))  # 裁剪区
            current_root = save_root + str(count + start_point).zfill(zfill_num) + ".jpg"
            region.save(current_root)  # str(i)是裁剪后的编号
            # count = count + 1
            #
            ####filter modification#####
            img = cv2.imread(current_root)
            img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            lower_blue = np.array([0, 0, 0])
            upper_blue = np.array([255, 255, 201])

            mask = cv2.inRange(img_hsv, lower_blue, upper_blue)

            mask_pix = 0
            for tof in range(width):
                for sat in range(width):
                    if mask[tof][sat] == 255:
                        mask_pix = mask_pix + 1
            print(mask_pix)
            if mask_pix > 1000:
                #there is useful element in the pic
                count = count + 1
            #####end filter modification #####
            #note: if you wish to eliminate blank filter, remember to add the counter back to the main frame



    #print("end_point:",col*row+start_point)
    print("end point: ",count)
    print("finish")

def cal_resize(img_root, mul_rate, width, height, overlap_x, overlap_y):
    im = Image.open(img_root)
    xorigin = im.size[0]/mul_rate
    yorigin = im.size[1]/mul_rate
    start_loc_x = int(width * (1 - overlap_x))
    start_loc_y = int(height * (1 - overlap_y))
    x = math.ceil((xorigin-width)/(start_loc_x))*start_loc_x+width
    y = math.ceil((yorigin-height)/(start_loc_y))*start_loc_y+height
    resize = [x,y]
    return resize

if __name__ == "__main__":
    img_root = "ssj.jpg"  # 原始图片路径
    width = 256  # 设置你要裁剪的小图的宽度
    height = 256  # 设置你要裁剪的小图的高度
    overlap_rate = 3 / 4  # 等于 overlap_rate_y
    start_point = 0  # 序号从第n张开始保存，默认为0；若要从第01234.jpg开始保存，则 start_point 为 1234
    zfill_num = 5  # 文件名长度，如 00011.jpg 的 zfill_num 为 5
    save_root = "./0511_multi_tr/"

    # 单条裁剪
    # ver_cut(img_root, width, height, overlap_rate, save_root, start_point, zfill_num)

    # For Wuyong & Shengshan
    # resize = (4096, 2560)  # For multiscaling
    mul_rate =  2           # For multiscaling 即裁出来的256图包含最开始256图信息的比例
    overlap_x = 3/4
    overlap_y = 3/4

    print("img_root:",img_root)
    print("start_point:",start_point)
    print("mul_rate:",mul_rate)
    resize = cal_resize(img_root, mul_rate, width, height, overlap_x, overlap_y)
    total_cut(img_root, resize,width, height, overlap_x, overlap_y, save_root, start_point, zfill_num)
