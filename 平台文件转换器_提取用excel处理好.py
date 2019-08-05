# -*- coding:utf-8 -*-
# Gene assignment split in annotation

import pandas as pd
import datetime

file_path = input("请输入文件路径（直接复制文件管理器上的路径）：")
name = input("请输入文件名（不加后缀名）：")

file_name = file_path + '\\' +name + '.txt'

ann = pd.read_csv(file_name, sep='\t', index_col=0)

start_time = datetime.datetime.now()
count = 0

for i in range(len(ann.index)):
    string = ann.iloc[i].values.tolist()[0]
    if isinstance(string, str):
        if '//' in string:
            count += 1
            name = string.split()[2]
            ann.iloc[i] = name
            print('第%d个id转换完成，转换名为%s' % (count, name))


end_time = datetime.datetime.now()
t_s = (end_time - start_time).seconds
t_min = t_s // 60

if t_min == 0:
    if t_s <= 1:
        print("处理%d个gene耗时不超过1秒。" % count)
    else:
        print("处理%d个gene共耗时%d秒。" % (count, t_s))
else:
    print("处理%d个gene共耗时%d分%d秒。" % (count, t_min, (t_s - t_min*60)))

# Save file
new_name = file_name.split(sep='.txt')[0] + 'new.txt'
ann.to_csv(new_name, sep='\t')
