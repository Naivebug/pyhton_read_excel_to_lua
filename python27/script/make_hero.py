# coding:utf-8
'''
#create by NaiveBug^梁疯
'''
from makescript import *

def DaoBiao():
    #--------导出mkdata_hero单个文件..
    FileName = "英雄导表.xlsx"
    sheetName = "英雄"
    TestPrint("----开始分页:", FileName, sheetName)
    title = ['SID',    'Name',    'HP',    'BaseAtk',    'list1',    'map1', ];  # 可修改
    string = ["Name", ];  # 字符串类型,可修改
    tuples = ["list1",'map1',];  # 列表或元组类型可修改
    floats = []
    dataName = "mkdata_hero" #输出名字
    data = ReadTitle2Dict(FileName,sheetName,title,string,tuples,floats,dataName,noReadRow = 2)
    data = Change2LuaData(data,title,dataName)
    MakeData2File(data,'data/%s.lua' % dataName,dataName,dataName)
    TestPrint("==导表分页OK:", FileName, sheetName)
    #--------导出mkdata_monster单个文件..
    FileName = "英雄导表.xlsx"
    sheetName = "怪物"
    TestPrint("----开始分页:", FileName, sheetName)
    title = ['SID',    'Name',    'HP',    ];  # 可修改
    string = ["Name", ];  # 字符串类型,可修改
    tuples = [];  # 列表或元组类型可修改
    floats = []
    dataName = "mkdata_monster" #输出名字
    data = ReadTitle2Dict(FileName,sheetName,title,string,tuples,floats,dataName,noReadRow = 2)
    data = Change2LuaData(data,title,dataName)
    MakeData2File(data,'data/%s.lua' % dataName,dataName,dataName)
    TestPrint("==导表分页OK:", FileName, sheetName)
    #-----------------------导出多个文件模式----------------
    FileName = "英雄导表.xlsx"
    sheetName = "英雄"
    TestPrint("----开始多文件分页:", FileName, sheetName)
    title = ['SID',    'Name',    'HP',    'BaseAtk',    'list1',    'map1', ];  # 可修改
    string = ["Name", ];  # 字符串类型,可修改
    tuples = ["list1",'map1',];  # 列表或元组类型可修改
    floats = []
    # 战斗时用
    module1, moudue2 = 'npc', 'pet'  # 只修改这个即可
    data = ReadMoreFile(FileName, sheetName, title,noReadRow = 2);
    PubMakeMoreFile(data, title, string, tuples, floats, module1, moudue2, strClassNameFlag="" ) #pathoutadd='war/'
    TestPrint("----导表多文件分页OK:", FileName, sheetName)
   
   



