# -*- coding: utf-8 -*-
'''
#create by NaiveBug^梁疯
'''


def GBK2UTF8(s):
    # print("s",s)
    # print(help(str))
    # s = s.decode('utf-8').encode('gb2312')
    return s
def Start(ReadPath,PathOut):
    print("--------start------------")
    ls = {#描述作用
            0:"0:所有配置表",
            1:"1:英雄表",
            2:"2:技能表",
        }
    keys = sorted(ls.keys())
    for k in keys:
        print( GBK2UTF8(ls[k]) )
    s = input("你好 : ")
    print("s",s)

Start(0,1)