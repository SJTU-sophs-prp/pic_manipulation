import cv2 as cv
import os


def getAllImg(path):
    result = []
    filelist = os.listdir(path)
    for file in filelist:
        if os.path.isfile(os.path.join(path, file)):
            if file.split('.')[1] in ('jpg', 'png'):
                result.append(os.path.join(path, file))
    return result


def flip(path, name_len):
    list = getAllImg(path)
    list.sort()
    length = list.__len__()
    for i in range(length):
        img = cv.imread(list[i])
        new = cv.flip(img, 1)
        name = "./" + path + "/" + str(length+i).zfill(name_len) + ".jpg"
        cv.imwrite(name, new)


if __name__ == '__main__':
    path = "./test"  # 原图文件夹，需要满足 总共n张图片，最后一张的文件名是n-1.jpg
    name_len = 5  # 比如 00011.jpg 的话就是5

    flip(path, name_len)  # 最后将保存到原文件夹
    print("Finish")
