#!/usr/bin/python3
# -*- coding:utf-8 -*-
# @Author: Fishbony
# 识别pdf的名字然后进行重命名及转换成500ppi的jpg图片


import os
import pdf2image
from PIL import Image
import pytesseract
import matplotlib.pyplot as plt

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def transfer(filename):
    pil_img = pdf2image.convert_from_path(filename, dpi=500, fmt='jpg')
    for image in pil_img:
        image.save(filename[:-4] + ".jpg")


def ocr_img(img_name):
    img = Image.open(img_name)
    name_cell = img.crop((370, 1120, 1200, 1234))
    text = pytesseract.image_to_string(name_cell)
    if text == '':
        config_arg = ['--psm ' + str(i) for i in range(13)]
        for arg in config_arg:
            try:
                text = pytesseract.image_to_string(name_cell, config=arg, lang='chi_sim')
                print(arg, text)
            except:
                print('名字识别错误！')
            else:
                if text != '':
                    break

    if '\n' in text:
        text = ''.join(text.split('\n'))
    new_name = text + '.jpg'
    return new_name


def rename(filename):
    img_name = filename[:-4] + '.jpg'
    new_name = ocr_img(img_name)
    os.rename(img_name, new_name)


# 测试用
def show(img):
    plt.figure()
    plt.imshow(img)
    plt.show()


if __name__ == '__main__':
    dir_path = input('请输入pdf文件目录')
    os.chdir(dir_path)

    pdf_list = []

    for file in os.listdir('.'):
        if 'pdf' in file:
            pdf_list.append(file)

    for i in pdf_list:
        try:
            transfer(i)
            rename(i)
        except:
            print(i, '转换失败。')
