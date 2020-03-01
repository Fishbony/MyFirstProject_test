#!/usr/bin/python3
# -*- coding:utf-8 -*-
# @Author: Fishbony
# rename image file

import os
from PIL import Image
import pytesseract
import matplotlib.pyplot as plt
import time


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def chi_is(word):
    # check chinese
    new = ''
    for ch in word:
        if u'\u4e00' <= ch <= u'\u9fff':
            new += ch
    return new


def ocr_img(img_name):
    # ocr each cell with name, determine size of each cell
    img = Image.open(img_name)  # open img and cut cell
    name_cell = img.crop((370, 1120, 1200, 1234))
    text = pytesseract.image_to_string(name_cell, config='--psm 8', lang='chi_sim')
    text = ''.join(text.split())
    text = chi_is(text) + '.jpg'
    if text == '':
        text = img_name
        print('%s fail' % img_name)
    return text


def rename(filename):
    new_name = ocr_img(img_name)
    os.rename(filename, new_name)


def show(img):
    # for test
    plt.figure()
    plt.imshow(img)  # 展示
    plt.show()


if __name__ == '__main__':
    dir_path = input('Input your images directory: ')
    st = time.time()
    os.chdir(dir_path)
    jpg_list = os.listdir('.')
    count = 0
    for jpg in jpg_list:
        try:
            rename(jpg)
            count += 1
        except:
            print('%s rename fail!' % jpg)
    end = time.time()
    t = end - st
    print('%d cases were renamed successfully. %f s in total!' % (count, t))
