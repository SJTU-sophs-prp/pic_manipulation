import codecs
import json
import os
import math
from PIL import Image

def getAllImg(path):
    result = []
    filelist = os.listdir(path)
    for file in filelist:
        if os.path.isfile(os.path.join(path, file)):
            if file.split('.')[-1] in ('jpg', 'png'):
                result.append(os.path.join(path, file))
    return result

if __name__ == '__main__':
    # with open('ziming.json', 'r') as f:
    #     data = json.load(f)
    data = json.load(codecs.open('ziming.json', 'r', 'utf-8-sig'))
    points = []
    for i in data['shapes']:
        points.append(i['points'])
    compress_rate = 1


    # image cut & save
    img_root = "zm.jpg"
    save_root = "./zm/"
    img_in = Image.open(img_root)

    count = 0
    for j in points:
        a = math.floor(j[0][0] * compress_rate)
        b = math.floor(j[0][1] * compress_rate)
        c = math.floor(j[1][0] * compress_rate)
        d = math.floor(j[1][1] * compress_rate)
        region = img_in.crop((a, b, c, d))
        region = region.resize((256,256))
        region.save(save_root + str(count).zfill(4) + ".jpg")
        count = count + 1


    # combine
    # origin_img_root = "./labelme_xrq/ss3~1.jpg"
    # ori_img = Image.open(origin_img_root)
    # ori_width, ori_height = ori_img.size
    # load_path = "./0922test/save3/"
    # s = getAllImg(load_path)
    # s.sort()
    # length = len(s)
    #
    # for i in range(length):
    #     img = Image.open(s[i])
    #     width = math.floor((points[i][1][0]-points[i][0][0]) * compress_rate)
    #     height = math.floor((points[i][1][1]-points[i][0][1]) * compress_rate)
    #     img = img.resize((width, height))
    #
    #     w = math.floor(points[i][0][0] * compress_rate)
    #     h = math.floor(points[i][0][1] * compress_rate)
    #     ori_img.paste(img, (w, h), mask=None)
    #
    # ori_img.save("./test3.jpg")


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
