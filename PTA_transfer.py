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
    img_name = filename.split('\\')[-1][:-4] + '.jpg'
    # img_path = '.\\pics\\' + img_name
    for image in pil_img:
        image.save(img_name)
    end = time.time()
    c = end - start
    print('%s: %f s in total' % (img_name, c))


def multi_process(pdf_list):
    with multiprocessing.Pool() as p:
        p.map(transfer, pdf_list)


def main():
    wd = input('Please in put file directory:')
    pic_dir = wd + '\\' + 'pics'
    os.mkdir(pic_dir)
    pdf_list = []

    for root, dirs, files in os.walk(wd):
        for file in files:
            if '.pdf' in file:
                pdf_list.append(os.path.join(root, file))

    os.chdir(pic_dir)

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

    end = time.time()
    print('%d in total! %d transfer!' % (len(pdf_list), len(os.listdir('.'))))
    print('Done! %.2f s in total!' % (end - st))


if __name__ == '__main__':
    main()
