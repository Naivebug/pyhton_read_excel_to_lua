# coding:utf-8
'''
Created on 2013-5-9
@author: dell
'''
from makescript import *

def Auto():
    path = g_ReadPath                          
    dirs = os.listdir(path)                    
    for name in dirs:                             
        if (os.path.splitext(name)[1] == ".xls") and name[0] != "~":  
            TestPrint("name",name)
            AutoDaoBiao(name)
                                 
def AutoDaoBiao(fBasename):
    fname = g_ReadPath + fBasename
    bk = xlrd.open_workbook(GetDecodeStr(fname))
    namels = bk.sheet_names()
    for sheetName2 in namels:
        #if isinstance(sheetName2,unicode):
        #    sheetName2 = GetEncodeStr(sheetName2)
        if(not sheetName2.isalnum()):
            #TestPrint("--pass unicode sheetName",fBasename,sheetName2)
            continue
        TestPrint("sheetName",fBasename,sheetName2)
        sheetName = GetDecodeStr(sheetName2)
        try:
            sh = bk.sheet_by_name(sheetName) 
        except:
            TestPrint("no this sheet %s ,in %s named " % (fname, sheetName))
            return;
        sheetName = GetEncodeStr(sheetName2)
        if sheetName!='test' and sh.ncols >0 and sh.nrows >4 :
            AutoDaoBiaoSheet(fBasename,sheetName,sh)
     
def num_by_except(num,default):
    try:
        return int(num)
    except ValueError:
        return default

def AutoDaoBiaoSheet(fname,sheetName,sh):
    # if not sheetName == "more" :
    #     return; 
    titleC = []
    stringC = []
    tuplesC = []
    floatsC = []
    titleS = []
    stringS = []
    tuplesS = []
    floatsS = []
    _temGroup = {}  
    _temGroupV = 0;
    #--
    a1 = GetCellValue(sh,0,0)
    a2 = GetCellValue(sh,1,0)
    a3 = GetCellValue(sh,2,0)
    if a3 != "": a3 = num_by_except(a3,"")
    if not (a1.find("c") != -1 or a1.find("s") != -1 ) or a2 not in ["string","int","float"] or a3 not in [0,1,'0','1','0.0','1.0',] :
        TestPrint("--pass sheetName return",fname,sheetName)
        print("---heloo lost")
        #TestPrint("---aa",not (a1.find("c") != -1 or a1.find("s") != -1 ),a2 not in ["string","int","float"],a3,a3 not in ['0','1'])
        return
    for j in range(0,sh.ncols):
        stype1 =  GetCellValue(sh,0,j).strip()
        stype2 =  GetCellValue(sh,1,j).strip()
        stype3 =  num_by_except(GetCellValue(sh,2,j) or 0,0) 
        if stype1== "" or stype2 == "":continue
        stitle =  GetCellValue(sh,4,j).strip()
        #--
        if( stype3 >0  ) :
            _temGroupV = stype3
            if _temGroupV>2:_temGroupV = 2;
            if(_temGroup.get(stype3) == None): _temGroup[stype3] = []
            _temGroup[stype3].append(stitle)
        if stype1.find("c") != -1:
            if(stype3 == 0): titleC.append(stitle)
            if(stype2 == "str" or stype2 == "string" ): stringC.append(stitle)
            elif(stype2 == "float") : floatsC.append(stitle)
            elif(stype2  == "tuple" or stype2 == "list"): tuplesC.append(stitle)   
        if(stype1.find("s") != -1):
            if(stype3 == 0): titleS.append(stitle)
            if(stype2 == "str" or stype2 == "string" ): stringS.append(stitle)
            elif(stype2 == "float") : floatsS.append(stitle)
            elif(stype2  == "tuple" or stype2 == "list"): tuplesS.append(stitle)  
    #print("--_temGroup-",_temGroupV,_temGroup)
    newlinekeys = []
    if _temGroupV == 1:
        for k,v in _temGroup.items():
            titleC.append(v)
            titleS.append(v)
            newlinekeys.append(v[0])
    elif _temGroupV ==2:
        ls = []
        ls2 = ls
        for m in range(1,10):
            if(m in _temGroup):
                v = _temGroup[m]
                newlinekeys.append(v[0])
                if(len(ls)==0):
                    ls = v;
                    ls2 =v
                else:
                    ls2.append(v)
                    ls2 = v
        if len(ls) > 0 :
            print ("--ls",ls)
            titleC.append(ls)
            titleS.append(ls)
    #print("---newlinekeys",newlinekeys)
    TestPrint("--正在导出分页:", fname, sheetName,titleS)
    dataName = "mkdata_" + sheetName
    if(len(titleS) > 0 ):
        #TestPrint("-server:",titleS,stringS,tuplesS,floatsS)
        if _temGroupV==1:
            data = ReadTitleDictList(fname,sheetName,titleS,stringS,tuplesS,floatsS,dataName,noReadRow = 5);
        elif _temGroupV == 2:
            data = ReadTitleDictDictDict(fname,sheetName,titleS,stringS,tuplesS,floatsS,dataName,noReadRow = 5);
        else:
            data = ReadTitle2Dict(fname,sheetName,titleS,stringS,tuplesS,floatsS,dataName,noReadRow = 5);
        #MakeData2FileTS(data,'server/mkdata/%s.ts' % dataName,dataName,dataName);
        #print("----data:",data)

        data = Change2LuaData(data,titleS,dataName,newlinekeys)
        MakeData2File(data,'data/%s.lua' % dataName,dataName,dataName)
        TestPrint("++成功导出分页:", fname, sheetName,titleS)
    if(False and len(titleC) > 0 ):
        #TestPrint("-client:",titleC,stringC,tuplesC,floatsC)
        if _temGroupV==1:
            data = ReadTitleDictList(fname,sheetName,titleC,stringC,tuplesC,floatsC,"",noReadRow = 5);
        elif _temGroupV == 2:
            data = ReadTitleDictDictDict(fname,sheetName,titleC,stringC,tuplesC,floatsC,"",noReadRow = 5);
        else:
            data = ReadTitle2Dict(fname,sheetName,titleC,stringC,tuplesC,floatsC,"",noReadRow = 5);
        MakeData2FileTS(data,'client/mkdata/%s.ts' % dataName,dataName,dataName);
    
    
        