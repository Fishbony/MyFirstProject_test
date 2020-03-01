#!/usr/bin/python3
# -*- coding:utf-8 -*-
# @Author: Fishbony
# Script for OCR

import os
import pandas as pd
import pytesseract
from PIL import Image
import time
import matplotlib.pyplot as plt
import multiprocessing

# input location of tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def initial_one_patient(filename):
    """generate a Series to save hearing level data.
    Size of series is 24."""

    patient_name = filename[:-4]
    index_list = []

    x = 125
    for i in range(7):
        each_item = 'right_' + str(x) + '_AC'
        x *= 2
        index_list.append(each_item)

    x = 250
    for i in range(5):
        each_item = 'right_' + str(x) + '_BC'
        x *= 2
        index_list.append(each_item)

    x = 125
    for i in range(7):
        each_item = 'left_' + str(x) + '_AC'
        x *= 2
        index_list.append(each_item)

    x = 250
    for i in range(5):
        each_item = 'left_' + str(x) + '_BC'
        x *= 2
        index_list.append(each_item)

    p_series = pd.Series(index=index_list)
    p_series.name = patient_name

    return p_series


def fre_loc():
    """ Input the location in pics of PTA jpg.
    Return a list with 3 items. Each items contain a list of location dict."""

    ac_location = [
        {'frequency': 'right_125_AC', 'x': 630, 'y': 3833},
        {'frequency': 'right_250_AC', 'x': 630, 'y': 3920},
        {'frequency': 'right_500_AC', 'x': 630, 'y': 4005},
        {'frequency': 'right_1000_AC', 'x': 630, 'y': 4090},
        {'frequency': 'right_2000_AC', 'x': 630, 'y': 4170},
        {'frequency': 'right_4000_AC', 'x': 630, 'y': 4255},
        {'frequency': 'right_8000_AC', 'x': 630, 'y': 4340},
        {'frequency': 'left_125_AC', 'x': 2660, 'y': 3833},
        {'frequency': 'left_250_AC', 'x': 2660, 'y': 3920},
        {'frequency': 'left_500_AC', 'x': 2660, 'y': 4005},
        {'frequency': 'left_1000_AC', 'x': 2660, 'y': 4090},
        {'frequency': 'left_2000_AC', 'x': 2660, 'y': 4170},
        {'frequency': 'left_4000_AC', 'x': 2660, 'y': 4255},
        {'frequency': 'left_8000_AC', 'x': 2660, 'y': 4340}
    ]

    left_bc_location = [
        {'frequency': 'left_250_BC', 'x': 3280, 'y': 3833},
        {'frequency': 'left_500_BC', 'x': 3280, 'y': 3920},
        {'frequency': 'left_1000_BC', 'x': 3280, 'y': 4005},
        {'frequency': 'left_2000_BC', 'x': 3280, 'y': 4090},
        {'frequency': 'left_4000_BC', 'x': 3280, 'y': 4170}
    ]

    right_bc_location = [
        {'frequency': 'right_250_BC', 'x': 1250, 'y': 3833},
        {'frequency': 'right_500_BC', 'x': 1250, 'y': 3920},
        {'frequency': 'right_1000_BC', 'x': 1250, 'y': 4005},
        {'frequency': 'right_2000_BC', 'x': 1250, 'y': 4090},
        {'frequency': 'right_4000_BC', 'x': 1250, 'y': 4170}
    ]

    return [ac_location,
            left_bc_location,
            right_bc_location]


def check_bc(filename):
    """checking if there is a bone conducting"""
    img = Image.open(filename)

    # crop left bc img
    left_bc = img.crop((3119, 3833, 3433, 4226))
    l_result = pytesseract.image_to_string(left_bc)

    # crop right bc img
    right_bc = img.crop((1090, 3833, 1422, 4226))
    r_result = pytesseract.image_to_string(right_bc)

    # decision
    if l_result == '':
        if r_result == '':
            result = 3
            print('%s did not measure bc.' % filename[:-4])
        else:
            result = 2
            print('%s only measured right side bc.' % filename[:-4])
    else:
        if r_result == '':
            result = 1
            print('%s only measured left side bc.' % filename[:-4])
        else:
            result = 0
            print('%s has measured both side bc' % filename[:-4])

    return result


def verify_result(ig_class, result):
    """verifying the ocr result
    :param ig_class: Image class
    :type result: string
    """
    config_list = ['--psm ' + str(i) for i in range(1, 14)]
    # lang_list = ['eng', 'chi_sim']

    if result == '':
        for psm in config_list:
            try:
                result = pytesseract.image_to_string(ig_class, config=psm)
            except:
                pass
            if result.isdigit() or result == '-5':
                result = int(result)
                if result < 130 and result % 5 == 0:
                    return result

    if result.isdigit() or result == '-5':
        result = int(result)
        if result < 130 and result % 5 == 0:
            return result
        else:
            result = pytesseract.image_to_string(ig_class, config='--psm 7', lang='chi_sim')
            if result.isdigit() or result == '-5':
                result = int(result)
                if result < 130 and result % 5 == 0:
                    return result
                else:
                    result = 'Wrong'
                    print('Wrong recognition number!')
                    return result
    else:
        for psm in config_list:
            try:
                result = pytesseract.image_to_string(ig_class, config=psm)
            except:
                pass
            if result.isdigit():
                result = int(result)
                if result < 130 and result % 5 == 0:
                    return result
        try:
            result = pytesseract.image_to_string(ig_class, config='--psm 7', lang='chi_sim')
        except:
            pass

    result = ''.join(result.split())

    return result


def ocr_each_cell(filename, freq_loc):
    """
    :type freq_loc: dict
    :type filename: img file
    """
    img = Image.open(filename)
    # cropping size 180*60
    cell = img.crop((freq_loc.get('x'), freq_loc.get('y'), freq_loc.get('x') + 180, freq_loc.get('y') + 60))
    cell_name = filename[:-4] + '_cell.png'
    cell.save(cell_name, dpi=(300, 300))
    cell = Image.open(cell_name)
    # ocr cell to return a string which is a digit or chinese character.
    text = pytesseract.image_to_string(cell)
    text = verify_result(cell, text)
    print('%s is recogized as' % freq_loc.get('frequency'), text)
    os.remove(cell_name)
    return {freq_loc.get('frequency'): text}


def get_each_data(filename):
    each_pta = initial_one_patient(filename)
    bc_result = check_bc(filename)
    if bc_result == 0:
        for each_conduct_result in fre_loc():  # each_conduct_result是一个列表字典
            for each_result in each_conduct_result:  # each_result是一个字典
                cell_data = ocr_each_cell(filename, each_result)
                c_k = list(cell_data.keys())[0]
                c_v = list(cell_data.values())[0]
                each_pta[c_k] = c_v
        print("识别数目：", each_pta.size)

    elif bc_result == 1:  # 只是左边骨导做了

        target_list = fre_loc()[0] + fre_loc()[1]

        for each_result in target_list:
            cell_data = ocr_each_cell(filename, each_result)
            c_k = list(cell_data.keys())[0]
            c_v = list(cell_data.values())[0]
            each_pta[c_k] = c_v
        print("识别数目：", each_pta.size)
        # 填写右边的骨导
        for each_result in fre_loc()[2]:
            name = list(each_result.values())[0]
            n_name = name[:-2] + 'AC'
            each_pta[name] = 'notest'

    elif bc_result == 2:  # 只是右边

        target_list = fre_loc()[0] + fre_loc()[2]

        for each_result in target_list:
            cell_data = ocr_each_cell(filename, each_result)
            c_k = list(cell_data.keys())[0]
            c_v = list(cell_data.values())[0]
            each_pta[c_k] = c_v
        print("识别数目：", each_pta.size)
        # 填写左边骨导
        for each_result in fre_loc()[1]:
            name = list(each_result.values())[0]
            n_name = name[:-2] + 'AC'
            each_pta[name] = 'notest'
        print("完成骨导填充")

    else:
        # 双侧均未做
        target_list = fre_loc()[0]
        for each_result in target_list:
            cell_data = ocr_each_cell(filename, each_result)
            c_k = list(cell_data.keys())[0]
            c_v = list(cell_data.values())[0]
            each_pta[c_k] = c_v
        print("识别数目：", each_pta.size)

        for each_result in (fre_loc()[1] + fre_loc()[2]):
            name = list(each_result.values())[0]
            n_name = name[:-2] + 'AC'
            each_pta[name] = 'notest'
        print("完成骨导填充")

    return each_pta


def test(img):
    plt.figure()
    plt.imshow(img)
    plt.show()


def multi_main():
    print('广东省人民医院听力室PTA的pdf文件批量识别数据生成excel表格')
    print('====================================1.0版本==========================================')
    print(r'文件所在路径格式，从资源管理器拷贝过来，示例：E:\Article\My-Article\PDF_reading_project')
    print('\n')
    pic_path = input('Please input the images path:')

    os.chdir(pic_path)
    pic_list = os.listdir('.')
    st = time.time()
    # multiprocessing
    pool = multiprocessing.Pool()
    dt = pool.map(get_each_data, pic_list)
    dt = pd.DataFrame(dt)
    dt.to_csv('000_pta_excel.csv', sep=',', encoding='utf_8_sig')
    dt.to_csv('000_pta_dtat.txt', sep='\t')
    end = time.time()
    fxxk = end - st
    print('Done! csv file saved in directory.\n %.2f s in total!' % fxxk)


def main():
    print('广东省人民医院听力室PTA的pdf文件批量识别数据生成excel表格')
    print('====================================1.0版本==========================================')
    print(r'文件所在路径格式，从资源管理器拷贝过来，示例：E:\Article\My-Article\PDF_reading_project')
    print('\n')
    pic_path = input('Please input the images path:')

    os.chdir(pic_path)
    pic_list = os.listdir('.')
    dt = []
    st = time.time()

    for each_pic in pic_list:
        print('%s is being recognized...' % each_pic[:-4])
        try:
            dt.append(get_each_data(each_pic))
        except:
            print('%s failed. Please check this file!' % each_pic[:-4])

    dt = pd.DataFrame(dt)
    dt.to_csv('000_pta_excel.csv', sep=',', encoding='utf_8_sig')
    dt.to_csv('000_pta_dt.txt', sep='\t')
    end = time.time()
    fxxk = end - st
    print('Done! csv file saved in directory.\n %.2f s in total!' % fxxk)


if __name__ == '__main__':
    c = input("multiprocessing?(y or n)")
    if c == 'y':
        print('Multiprocessing...')
        multi_main()
        # 369.76 s in total! Saving img.

    else:
        print('Non-multiprocessing...')
        main()
        #  697.76 s in total! No saving img.
        # 525.41 s in total! Saving img.
