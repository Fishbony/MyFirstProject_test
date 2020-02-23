#!/usr/bin/python3
# -*- coding:utf-8 -*-
# @Author: Fishbony

import os
import shutil
import pdf2image


def transfer(filename):
    pil_img = pdf2image.convert_from_path(filename, dpi=500, fmt='jpg')
    for image in pil_img:
        image.save(filename[:-4] + ".jpg")


if __name__ == '__main__':
    dir_path = input('Please input pdf file directory:')
    os.chdir(dir_path)

    pdf_list = []
    for file in os.listdir('.'):
        if 'pdf' in file:
            pdf_list.append(file)
    os.mkdir('.\\pics')

    for pdf in pdf_list:
        transfer(pdf)
        img_name = pdf[:-4] + '.jpg'
        new_name = '.\\pics\\' + img_name
        shutil.move(img_name, new_name)

    print('Done!')
