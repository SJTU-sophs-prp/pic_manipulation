import cv2
import os
import time
from PIL import Image


def mix(img1_path, img2_path, Overlap_rate):
    img1 = Image.open(img1_path)
    img2 = Image.open(img2_path)
    img1_size = img1.size
    img2_size = img2.size
    w1 = img1_size[0]
    h1 = img1_size[1]
    w2 = img2_size[0]
    h2 = img2_size[1]

    upper_part = img1.crop((0, 0, w1, h1 - int(h2 * Overlap_rate)))
    mix_region1 = img1.crop((0, h1 - int(h2 * Overlap_rate), w1, h1))
    mix_region2 = img2.crop((0, 0, w2, int(h2 * Overlap_rate)))
    lower_part = img2.crop((0, int(h2 * Overlap_rate), w2, h2))

    temp_path = "./temp/"
    upper_part.save(temp_path + "A.jpg")
    mix_region1.save(temp_path + "B.jpg")
    mix_region2.save(temp_path + "C.jpg")
    lower_part.save(temp_path + "D.jpg")
    time.sleep(0.01)

    mix1 = cv2.imread(temp_path + "B.jpg")
    mix2 = cv2.imread(temp_path + "C.jpg")
    mix = cv2.addWeighted(mix1, Overlap_rate, mix2, 1 - Overlap_rate, 0)
    cv2.imwrite(temp_path + "M.jpg", mix)

    imgA = Image.open(temp_path + "A.jpg")
    imgM = Image.open(temp_path + "M.jpg")
    imgB = Image.open(temp_path + "D.jpg")
    sizeA = imgA.size
    sizeM = imgM.size
    joint = Image.new('RGB', (sizeA[0], int(sizeA[1] + sizeM[1] * (1 / Overlap_rate))))
    loc1, loc2, loc3 = (0, 0), (0, sizeA[1]), (0, sizeA[1] + sizeM[1])
    joint.paste(imgB, loc3)
    joint.paste(imgM, loc2)
    joint.paste(imgA, loc1)
    joint.save(temp_path + "Out.jpg")
    time.sleep(0.01)


def mix_hor(img1_path, img2_path, overlap_rate):
    img1 = Image.open(img1_path)
    img2 = Image.open(img2_path)
    img1_size = img1.size
    img2_size = img2.size
    w1 = img1_size[0]
    h1 = img1_size[1]
    w2 = img2_size[0]
    h2 = img2_size[1]
    left_part = img1.crop((0, 0, w1 - int(w2 * overlap_rate), h1))
    mix_region1 = img1.crop((w1 - int(w2 * overlap_rate), 0, w1, h1))
    mix_region2 = img2.crop((0, 0, int(w2 * overlap_rate), h2))
    right_part = img2.crop((int(w2 * overlap_rate), 0, w2, h2))

    temp_path = "./temp/"
    left_part.save(temp_path + "A.jpg")
    mix_region1.save(temp_path + "B.jpg")
    mix_region2.save(temp_path + "C.jpg")
    right_part.save(temp_path + "D.jpg")
    time.sleep(0.01)

    mix1 = cv2.imread(temp_path + "B.jpg")
    mix2 = cv2.imread(temp_path + "C.jpg")
    mix = cv2.addWeighted(mix1, 0.5, mix2, 0.5, 0)
    cv2.imwrite(temp_path + "M.jpg", mix)

    imgA = Image.open(temp_path + "A.jpg")
    imgM = Image.open(temp_path + "M.jpg")
    imgB = Image.open(temp_path + "D.jpg")
    sizeA = imgA.size
    sizeM = imgM.size
    sizeB = imgB.size
    joint = Image.new('RGB', (sizeA[0] + sizeM[0] + sizeB[0], sizeA[1]))
    loc1, loc2, loc3 = (0, 0), (sizeA[0], 0), (sizeA[0] + sizeM[0], 0)
    joint.paste(imgB, loc3)
    joint.paste(imgM, loc2)
    joint.paste(imgA, loc1)
    joint.save(temp_path + "Out.jpg")

    os.remove("./temp/A.jpg")
    os.remove("./temp/B.jpg")
    os.remove("./temp/C.jpg")
    os.remove("./temp/D.jpg")
    os.remove("./temp/M.jpg")


def getAllImg(path):
    result = []
    filelist = os.listdir(path)
    for file in filelist:
        if os.path.isfile(os.path.join(path, file)):
            if file.split('.')[1] in ('jpg', 'png'):
                result.append(os.path.join(path, file))
    return result


if __name__ == '__main__':

    # 参数调节如下 #
    path = "./zm_stage2"  # 原散装图文件夹
    all_pics = 17  # 2257  # 裁好的照片的总数
    height = 17  # 37  # 行数
    width = 1  # 61  # 列数
    overlap_rate_x = 3 / 4  # (256 - 50) / 256  # 横向重叠像素比
    overlap_rate_y = 3 / 4  # (256 - 50) / 256  # 纵向重叠像素比
    n = 0  # 中断后从第n张开始继续拼，默认从0开始
    output = "./test.jpg"  # 最后保存的路径


    ### 先纵向拼 ###
    s = getAllImg(path)
    s.sort()

    for i in range(all_pics):
        if i % height == 0 and i >= n * height:
            list = s[i:i + height]
            mix(list[0], list[1], overlap_rate_y)
            for j in range(2, height):
                mix("./temp/out.jpg", list[j], overlap_rate_y)
                time.sleep(0.01)  # wait for fileIO

            new_name = "./temp/out" + str(int(i / height)).zfill(2) + ".jpg"  # 每一条都存在temp文件夹里
            os.rename("./temp/out.jpg", new_name)

    os.remove("./temp/A.jpg")
    os.remove("./temp/B.jpg")
    os.remove("./temp/C.jpg")
    os.remove("./temp/D.jpg")
    os.remove("./temp/M.jpg")


    ### 再横向拼 ###
    ss = getAllImg("./temp/")
    ss.sort()
    list = ss[:]

    mix_hor(list[0], list[1], overlap_rate_x)

    for j in range(1, width - 1):
        mix_hor("./temp/Out.jpg", list[j + 1], overlap_rate_x)
        time.sleep(0.01)  # wait for fileIO

    os.rename("./temp/Out.jpg", output)

    for i in list:
        os.remove(i)

    ### 如果只需要拼一条，请把“再横向拼”部分注释掉，生成图在"./temp"文件夹里 ###

    print("finish")
