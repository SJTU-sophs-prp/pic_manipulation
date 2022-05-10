import os

from PIL import Image

Image.MAX_IMAGE_PIXELS = None
import math


def ver_cut(img_root, width, height, overlap_rate, save_root):
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
        region.save(save_root + str(j).zfill(3) + ".jpg")
    print("finish")


def total_cut(img_root, resize, width, height, overlap_x, overlap_y, save_root):
    im = Image.open(img_root)
    im = im.resize(resize)
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

    for i in range(col):
        for j in range(row):
            x = start_loc_x * i  # 裁剪起点的x坐标范围
            y = start_loc_y * j  # 裁剪起点的y坐标范围
            region = im.crop((x, y, x + w, y + h))  # 裁剪区
            region.save(save_root + str(row * i + j).zfill(4) + ".jpg")  # str(i)是裁剪后的编号
            # img = cv2.imread(save_root + str(row * i + j).zfill(4) + ".jpg", 0)  # 进行边缘提取
            # img_color = img
            # blur = cv2.GaussianBlur(img, (3, 3), 0)
            # canny = cv2.Canny(blur, 250, 250)
            # im2 = Image.fromarray(canny)  # 为了直观感受 canny 转化成图像
            # im2.save(save_root + str(row * i + j).zfill(4) + ".jpg")  # 存储成为图像的边缘图
    print("finish")


if __name__ == "__main__":
    img_root = "SSJ.jpg"  # 原始图片路径
    width = 256  # 设置你要裁剪的小图的宽度
    height = 256  # 设置你要裁剪的小图的高度
    overlap_rate = 1 / 2
    save_root = "./SSJ/"

    # For single strip
    # ver_cut(img_root, width, height, overlap_rate, save_root)

    # For Wuyong & Shengshan
    resize = (4096, 2560)
    overlap_x = 3/4
    overlap_y = 3/4
    total_cut(img_root, resize, width, height, overlap_x, overlap_y, save_root)
