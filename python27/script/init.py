# -*- coding: utf-8 -*-
'''
#create by NaiveBug^梁疯
'''
import makescript 

def GBK2UTF8(s):
    s = s.decode('utf-8').encode('gb2312')
    return s
def Start(ReadPath,PathOut):
    makescript.PathOut = PathOut
    makescript.ReadPath = ReadPath
    makescript.g_PathOut = PathOut
    makescript.g_ReadPath = ReadPath
    input = -1;
    while True:
        print "--------start------------"
        ls = {#描述作用
                0:"0:所有配置表",
                1:"1:英雄表",
                2:"2:技能表",
            }
        keys = sorted(ls.keys())
        for k in keys:
            print GBK2UTF8(ls[k])
        str = raw_input(GBK2UTF8("不输入就编译所有,输入编号就仅编译指定文件:, \n"));  
        print "Received input is : ", str  
        if str != "":
            input = int(str); 
            if ls.has_key(input) :
                break
            else:
                print GBK2UTF8("error:输入有误,请输入正确的数字编号")
        else:#输入了Enter
            input = 0;
            break
    if input in [0,1]:#英雄
        import make_hero
        make_hero.DaoBiao()
    if input in [0,2]:#技能
        #import make_skill
        #make_skill.DaoBiao()
        pass