#!/usr/bin/python3
# -*- coding:utf-8 -*-
# @Author: Fishbony

import os
import shutil
import pdf2image
import time
import multiprocessing


def transfer(filename):
    start = time.time()
    print("%s transfering..." % filename)
    pil_img = pdf2image.convert_from_path(filename, dpi=500, fmt='jpg')
    for image in pil_img:
        image.save(filename[:-4] + ".jpg")
    end = time.time()
    c = end - start
    print('%s: %f s in total' % (filename, c))


def multi_process(pdf_list):
    with multiprocessing.Pool() as p:
        p.map(transfer, pdf_list)


def main():
    wd = input('Please in put file directory:')
    os.chdir(wd)
    pdf_list = os.listdir('.')
    c = input('Multiprocessing (y or n)')
    st = time.time()
    if c == 'y':
        # 297.03s in total 5 cases
        multi_process(pdf_list)
    else:
        for pdf in pdf_list:
            try:
                # 323.36 s in total 5 cases
                transfer(pdf)
            except:
                print('%s transfer fail! Please check the file.' % pdf[:-4])
    # move into directory
    os.makedirs('./pics')
    pic_list = [jpg for jpg in os.listdir('.') if 'jpg' in jpg]
    for pic in pic_list:
        dst = './pics/' + pic
        shutil.move(pic, dst)
    end = time.time()
    print('Done! %.2f s in total!' % (end - st))


if __name__ == '__main__':
    main()