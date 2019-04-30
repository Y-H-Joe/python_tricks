# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 10:33:28 2019

@author: Yihang Zhou
"""
"""
####========Readme========####
本脚本根据关键字从目标文件夹中找到文件，复制到当作路径下的filtered_files文件里。关键字是并集
的关系，比如关键字为 apple和pear，那名字中包含apple或者pear的文件都会被复制。在filtered_files
中的重命文件会被overwritten

使用示例：
python check_filename.py ~/NaoJiYe/ ~/NaoJiYe/scRNA_data_all ~/NaoJiYe/keyword.csv 20181008_CSF_1

参数说明：
第一个参数为工作路径
第二个参数为你想要遍历寻找的目标文件夹
第三个参数为keyword.csv所在的全路径
第四个参数为用来装输出文件的文件夹名

keyword.csv：
表头输入name
在name这一列下面输入你的关键字，一个关键字占一行
"""
import os,sys
import pandas as pd
import shutil

datapath=sys.argv[1]
os.chdir(datapath)
datapath=datapath.strip().rstrip("\\") ## 去除首位空格和尾部 \ 符号
filtered_files=str(datapath+'/'+sys.argv[4])
if not os.path.exists(filtered_files):
    print(datapath," does not exist, mkdir now.")
    os.makedirs(filtered_files)
file_path=sys.argv[2]  #目标搜索的文件路径
filename_path=sys.argv[3]  #关键字csv所在位置

file_name=pd.read_csv(filename_path)   #读取所需文件列表
file_name['count']=0    #定义新的一列count，用于计数
file_name_rows=file_name.shape[0]   #表格的行数
for root,dirs,files in os.walk(file_path):
    for name in files:
        olddir=os.path.join(root,name) #每一个文件路径    
        for i in range(file_name_rows):
            if str(file_name['name'][i]) in name:   #寻找对应的文件名
                print("olddir: ",olddir)
                newdir=os.path.join(filtered_files,name)
                print("newdir: ",newdir)
                shutil.copy(olddir,newdir)  #复制到新文件夹中
                #shutil.copy2(olddir,newdir) #升级版，能把文件最后访问时间与修改时间也复制过来
                file_name['count'][i]=file_name['count'][i]+1   #计数
                print("This file has been copied: ",name)  #打印出文件名
            else:
                continue

file_name.to_csv('file_name_count.csv')        #保存新的文件列表
