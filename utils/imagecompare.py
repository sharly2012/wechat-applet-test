# -*- coding: utf-8 -*-
import cv2
import numpy as np
from matplotlib import pyplot as plt

"""
用途：利用python实现多种方法来实现图像识别
author:SYW
"""


# 最简单的以灰度直方图作为相似比较的实现
def classify_gray_hist(image1, image2, size=(256, 256)):
    # 先计算直方图
    # 几个参数必须用方括号括起来
    # 这里直接用灰度图计算直方图，所以是使用第一个通道，
    # 也可以进行通道分离后，得到多个通道的直方图
    # bins 取为16
    # 返回值为0~1，值越大相似度越高
    image1 = cv2.resize(image1, size)
    image2 = cv2.resize(image2, size)
    hist1 = cv2.calcHist([image1], [0], None, [256], [0.0, 255.0])
    hist2 = cv2.calcHist([image2], [0], None, [256], [0.0, 255.0])
    # 可以比较下直方图
    plt.plot(range(256), hist1, 'r')
    plt.plot(range(256), hist2, 'b')
    plt.show()
    # 计算直方图的重合度
    degree = 0
    for i in range(len(hist1)):
        if hist1[i] != hist2[i]:
            degree = degree + (1 - abs(hist1[i] - hist2[i]) / max(hist1[i], hist2[i]))
        else:
            degree = degree + 1
    degree = degree / len(hist1)
    return degree


# 计算单通道的直方图的相似值
def calculate(image1, image2):
    hist1 = cv2.calcHist([image1], [0], None, [256], [0.0, 255.0])
    hist2 = cv2.calcHist([image2], [0], None, [256], [0.0, 255.0])
    # 计算直方图的重合度
    degree = 0
    for i in range(len(hist1)):
        if hist1[i] != hist2[i]:
            degree = degree + (1 - abs(hist1[i] - hist2[i]) / max(hist1[i], hist2[i]))
        else:
            degree = degree + 1
    degree = degree / len(hist1)
    return degree


# 通过得到每个通道的直方图来计算相似度
def classify_hist_with_split(image1, image2, size=(256, 256)):
    # 将图像resize后，分离为三个通道，再计算每个通道的相似值
    image1 = cv2.resize(image1, size)
    image2 = cv2.resize(image2, size)
    sub_image1 = cv2.split(image1)
    sub_image2 = cv2.split(image2)
    sub_data = 0
    for im1, im2 in zip(sub_image1, sub_image2):
        sub_data += calculate(im1, im2)
    sub_data = sub_data / 3
    return sub_data


# 平均哈希算法计算
def classify_aHash(image1, image2):
    image1 = cv2.resize(image1, (8, 8))  # cv2.resize(源，目标，变换方法),将图片变换成想要的尺寸
    image2 = cv2.resize(image2, (8, 8))
    # cv2.cvtColor(input_image,flag)实现图片颜色空间的转换，flag 参数决定变换类型。如 BGR->Gray flag
    # 就可以设置为 cv2.COLOR_BGR2GRAY 。
    gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
    hash1 = get_hash(gray1)
    hash2 = get_hash(gray2)
    return hamming_distance(hash1, hash2)


def classify_pHash(image1, image2):
    image1 = cv2.resize(image1, (32, 32))
    image2 = cv2.resize(image2, (32, 32))
    gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
    # 将灰度图转为浮点型，再进行dct变换
    dct1 = cv2.dct(np.float32(gray1))
    dct2 = cv2.dct(np.float32(gray2))
    # 取左上角的8*8，这些代表图片的最低频率
    # 这个操作等价于c++中利用opencv实现的掩码操作
    # 在python中进行掩码操作，可以直接这样取出图像矩阵的某一部分
    dct1_roi = dct1[0:8, 0:8]
    dct2_roi = dct2[0:8, 0:8]
    hash1 = get_hash(dct1_roi)
    hash2 = get_hash(dct2_roi)
    return hamming_distance(hash1, hash2)


# 输入灰度图，返回hash
def get_hash(image):
    average = np.mean(image)  # np.mean()求取均值
    hash = []
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            if image[i, j] > average:
                hash.append(1)
            else:
                hash.append(0)
    return hash


def hamming_distance(hash1, hash2):
    # 计算汉明距离
    # 返回值越小，图片相似度越高
    num = 0
    for index in range(len(hash1)):
        if hash1[index] != hash2[index]:
            num += 1
    return num


if __name__ == '__main__':
    img1 = cv2.imread('F:/test/1.png', cv2.IMREAD_COLOR)
    img2 = cv2.imread('F:/test/3.png', cv2.IMREAD_COLOR)
    c_img1 = img1[200:400, 500:800]  # 截取图片的某一部分
    c_img2 = img2[200:400, 500:800]  # syw,[200:400]控制的是高度，[500:800]控制的是长度，500代表的是x1，800代表的是x2
    cv2.imshow('img1', c_img1)  # 创建一个窗口显示图片，共2个参数，第一个参数为”窗口显示图片的标题“可以创建多个窗口，但每个窗口都不能重名，第二个参数为读入的图片
    cv2.imshow('img2', c_img2)
    degree1 = classify_gray_hist(img1, img2)
    degree2 = classify_hist_with_split(img1, img2)
    degree3 = classify_pHash(img1, img2)
    degree4 = classify_pHash(c_img1, c_img2)
    degree5 = classify_aHash(c_img1, c_img2)
    print(degree1)
    print(degree2)
    print(degree3)
    print(degree4)
    print(degree5)
    if degree5 == 0 or degree5 < 10:
        print("pass")
    else:
        print("fail")
    cv2.waitKey(0)
    cv2.destroyAllWindows()  # 删除建立的全部窗口
