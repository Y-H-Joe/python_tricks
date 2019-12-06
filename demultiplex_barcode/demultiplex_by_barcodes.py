# -*- coding: utf-8 -*-
"""
Created on Wed May 15 18:19:07 2019

@author: Y.H. Zhou

Contact: yihangjoe@foxmail.com
"""
"""
注意：
只能输入fq文件，gz不行
优点：
可以mismat
可以输出unmatched reads
有的read开头少测了一个，后面是正确的，这里就把开头的给补齐，覆写，可显著提高read利用率
缺点：
直接将fq文件读入内存，简单粗暴，服务器可用内存需要超过两个fq文件之和
单线程，速度较慢
warning:
认为可用read的第33位碱基是T，不是的话请手动修改，只可在此脚本上修改，不提供命令行接口
"""
import pandas as pd
import os,sys

if len(sys.argv)!=9:
    print("something wrong with the parameters.")
    sys.exit()

read1=sys.argv[1]
read2=sys.argv[2]
bpos=int(sys.argv[3])
blen=int(sys.argv[4])
bfil=sys.argv[5]
mis=int(sys.argv[6])
fix=int(sys.argv[7]) #只能是0或1，默认为1
datapath=sys.argv[8]
tpos=33#认为可用read的第33位碱基是T，不是的话请手动修改，只可在此脚本上修改，不提供命令行接口

datapath=datapath.strip().rstrip("/") ## 去除首位空格和尾部 / 符号
if not os.path.exists(datapath):
    print(datapath," does not exist, mkdir now.")
    os.mkdir(datapath)
os.chdir(datapath)

#根据barcode创建文件
bfil=list(pd.read_csv(bfil,header=None)[0])
read1_pre=".".join(read1.split("/")[-1].split(".")[:-1])
read2_pre=".".join(read2.split("/")[-1].split(".")[:-1])

with open(read1) as r1, open(read2) as r2:
    f1=r1.readlines()#内存爆炸,f1是list
    f2=r2.readlines()
    
    #4个一组
    a=0
    b=1
    c=2
    d=3
    
    while d<=len(f1):#还没有把文件跑到底的时候
        #mismatch
        f1_bar=f1[b][bpos-1:bpos-1+blen]#把f1的barcode给提出来
        #有的read开头少测了一个，后面是正确的，这里就把开头的给补齐，覆写，提高read利用率
        #有的read开头多测了一个，后面是正确的，这里就把开头的给覆写，提高read利用率
        #以上两个操作会改变fix长度的read长度，这里通过增减poly T来弥补
        #这是其他人的代码没有的
        f1_bar_fix_minus=f1[b][bpos-1-fix:bpos-1-fix+blen]
        f1_bar_fix_plus=f1[b][bpos-1+fix:bpos-1+fix+blen]
        #在barcode里循环查找匹配
        #match看有没有匹配上
        match=0
        for i in bfil:
            list_f1_bar=list(f1_bar)
            list_f1_bar_fix_minus=list(f1_bar_fix_minus)
            list_f1_bar_fix_plus=list(f1_bar_fix_plus)
            list_i=list(i)
            #two list comprehension
            #挨个看list里的item是否相等
            #如果mismatch匹配上了就写，退出for
            if sum([x==y for (x,y) in zip(list_f1_bar,list_i)]) >= (blen-mis):
                f1_bar=i
                with open(str(read1_pre+"_"+f1_bar+".fastq"),"a") as r1_in:
                    r1_in.write(f1[a])
                    r1_in.write(f1[b])
                    r1_in.write(f1[c])
                    r1_in.write(f1[d])
                with open(str(read2_pre+"_"+f1_bar+".fastq"),"a") as r2_in:
                    r2_in.write(f2[a])
                    r2_in.write(f2[b])
                    r2_in.write(f2[c])
                    r2_in.write(f2[d])
                #进入下一组
                a+=4
                b+=4
                c+=4
                d+=4
                match=1
                break
            #否则如果只是index少测了一个bp，匹配上了就写，退出for
            else:
                if sum([x==y for (x,y) in zip(list_f1_bar_fix_minus,list_i)]) >= (blen-mis):
                    f1_bar=i
                    with open(str(read1_pre+"_"+f1_bar+".fastq"),"a") as r1_in:
                        index=f1[a].split(":")[-1].strip() #f1[a]为@E00491:336:HVCJNCCXY:5:1101:16011:1555 1:N:0:TAAGGCGA
                        r1_in.write(f1[a])
                        list_f1_b=list(f1[b])
                        del(list_f1_b[tpos])#这里补了1个bp，所以为了总长不变删了一个T
                        fixed_seq=str(index+"".join(list_f1_b[len(index)-fix:]))
                        r1_in.write(fixed_seq)#开头重写为TAAGGCGA
                        r1_in.write(f1[c])
                        r1_in.write(f1[d])
                    with open(str(read2_pre+"_"+f1_bar+".fastq"),"a") as r2_in:
                        r2_in.write(f2[a])
                        r2_in.write(f2[b])
                        r2_in.write(f2[c])
                        r2_in.write(f2[d])
                    #进入下一组
                    a+=4
                    b+=4
                    c+=4
                    d+=4
                    match=1 
                    break
                if sum([x==y for (x,y) in zip(list_f1_bar_fix_plus,list_i)]) >= (blen-mis):
                    f1_bar=i
                    with open(str(read1_pre+"_"+f1_bar+".fastq"),"a") as r1_in:
                        index=f1[a].split(":")[-1].strip() #f1[a]为@E00491:336:HVCJNCCXY:5:1101:16011:1555 1:N:0:TAAGGCGA
                        r1_in.write(f1[a])
                        list_f1_b=list(f1[b])
                        list_f1_b.insert(tpos,"T")#这里删了1个bp，所以为了总长不变补了一个T
                        fixed_seq=str(index+"".join(list_f1_b[len(index)+fix:]))
                        r1_in.write(fixed_seq)#开头重写为TAAGGCGA                        
                        r1_in.write(f1[c])
                        r1_in.write(f1[d])
                    with open(str(read2_pre+"_"+f1_bar+".fastq"),"a") as r2_in:
                        r2_in.write(f2[a])
                        r2_in.write(f2[b])
                        r2_in.write(f2[c])
                        r2_in.write(f2[d])
                    #进入下一组
                    a+=4
                    b+=4
                    c+=4
                    d+=4
                    match=1 
                    break
        #真匹配不上了，把不match的，即有问题的read输出，这是其他人的代码没有的
        if not match:                    
            with open(str(read1_pre+"_"+"unmatched"+".FASTQ"),"a") as r1_in:
                r1_in.write(f1[a])
                r1_in.write(f1[b])
                r1_in.write(f1[c])
                r1_in.write(f1[d])
            with open(str(read2_pre+"_"+"unmatched"+".FASTQ"),"a") as r2_in:
                r2_in.write(f2[a])
                r2_in.write(f2[b])
                r2_in.write(f2[c])
                r2_in.write(f2[d])
            #进入下一组
            a+=4
            b+=4
            c+=4
            d+=4 
        


    
    