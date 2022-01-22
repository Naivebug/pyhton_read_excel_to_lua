# coding:utf-8
'''
#create by NaiveBug^梁疯
'''
from operator import truediv
import xlrd
import os
import slpp

keyline = 0; #关键字行放在第一行
g_encode = "utf-8";
g_ReadPath = ""
g_PathOut = ""
g_types = {}
g_bLua  = True

def is_num_by_except(num):
    try:
        int(num)
        return True
    except ValueError:
        return False

def SetKeysStr(keys,tems,string):
    # if keys in string: 
    #      strline = "\n \'%s\':{" % tems; 
    # else:
    #     strline = "\n%d:{" % int(tems);
    if keys in string:
        if is_num_by_except(tems) :
            return "\n%d:{" % int(tems); 
        else:
            return "\n\"%s\":{" % tems; 
    else:
        return "\n%d:{" % int(tems); 

def SetTypes(types):
    g_types = types

def SetPath(ReadPath, PathOut):  # 设置读和写的路径
    global g_ReadPath,g_PathOut
    if ReadPath[-1] != '/':
        ReadPath += '/'
    if PathOut[-1] != '/':
        PathOut += '/'
    g_ReadPath = ReadPath
    g_PathOut = PathOut;
    

def TestPrint(*msg):
    strmsg = ''
    for temmsg in msg:
        temmsg = str(temmsg)
        temmsg = GetDecodeStr(temmsg)
        strmsg += temmsg + ",";
    print ( strmsg )
    return 

# 编码 字符
def GetEncodeStr(temstr):
    #if isinstance(temstr,unicode):
    #    temstr = temstr.encode(g_encode)
    return temstr

# 译码,解码
def GetDecodeStr(temstr):
    #temstr = temstr.decode(g_encode)
    return temstr

def GetSheetInfo(fname,sheetName,title,noReadRow):
    fname = g_ReadPath + fname
    bk = xlrd.open_workbook(GetDecodeStr(fname))
    try:
        sh = bk.sheet_by_name(GetDecodeStr(sheetName))
    except:
        TestPrint("no this sheet %s ,in %s named " % (fname, sheetName))
        return;
    if sh.ncols < len(title):
        TestPrint(title)
        err = "%s,%s:tile num > cols are you delete col?" % (fname,sheetName);
        TestPrint(err)
        raise err;
    maptitle = {}
    subtitle = []
    if type(title[-1]) == tuple or  type(title[-1]) == list:
        subtitle = title[-1]
    temtitle = {};
    
    for stitle in title:
        while type(stitle) == list or type(stitle) == tuple:  
            temtuple = ""
            for key in stitle:
                if  type(key) == list or type(key) == tuple:   
                    temtuple = key
                else:
                    temtitle[key] = 1;
            stitle = temtuple
        if stitle != "":
            temtitle[stitle] = 1;
    for j in range(0,sh.ncols):
        Name =  GetCellValue(sh,noReadRow - 1,j)
        #Name =  GetCellValue(sh,keyline,j)
        if Name in temtitle  :
            maptitle[Name] = j;
    return sh,maptitle,subtitle
    
def GetCellValue(sh,i,j):
    tems = sh.cell_value(i,j)
    #if isinstance(tems,unicode):
    #    tems = tems.encode(g_encode);
    return tems

# def GetEvalStr(tems):
#     tems = eval(tems);
#     tems = slpp.SLPP().encode(tems);
#     return str(tems)

def GetEvalStr(tems,changelua=False):#Make More File的时候需要Change
    if isinstance(tems,float):tems = int(tems);
    tems = str(tems)
    if tems and tems[0] not in ['[','(','{']:
        tems = "[" + tems + ']'
    tems = eval(tems);
    if changelua:
        if tems:
            tems = slpp.SLPP().encode(tems);
        else:
            tems = {}
    return str(tems)

def ReadMoreFile(fname,sheetName,title,noReadRow = 2):
    sh,maptitle,subtitle = GetSheetInfo(fname,sheetName,title,noReadRow);
    nrows = sh.nrows
    data = {};
    keyid = title[0];  # 第一个默认为关键字
    for i in range(noReadRow,nrows):
        onelinedata = {};
        for keys in title:
            try:
                try:
                    j = maptitle[keys];
                except:
                    TestPrint("%s,%s表没有这个关键字:%s" % (fname, sheetName, keys))
                    raise 
                tems = GetCellValue(sh,i,j)
                onelinedata[keys] = tems
                if keys == keyid:
                    try:
                        if tems == "": break #会跨行
                        data[int(tems)] = onelinedata;
                    except:
                        TestPrint("%d行的数据异常" % (i + 1))
                        raise
            except:
                TestPrint("%s,%s,:%s,%d行出问题" % (fname, sheetName, keys, i + 1))
                raise 
    return data


def Change2LuaData(data,title,dataName,newlinekeys):#专门转换Map开头的函数的数据
    exec( data);
    data = slpp.SLPP().encode(eval(dataName),newlinekeys);
    data = "\n--%s\n" % (str(title)) + "return "  + data + "\n" #+ ChangeTitleData2Class(dataName,title) 
    LuaMakeRequirHead(dataName);
    return data;
    
def ChangeDict2LuaData(data,title,dataName):#专门转换Dict开头的函数的数据
    exec( data);
    data = slpp.SLPP().encode(eval(dataName));
    data = "\n--%s\n" % (str(title)) + "return "  + data + "\n" #+ ChangeTitleDictData2Class(dataName,title) 
    LuaMakeRequirHead(dataName);
    return data;

def ReadData2Map(fname,sheetName,title,string,tuples,dataName,noReadRow = 2):
    sh,maptitle,subtitle = GetSheetInfo(fname,sheetName,title,noReadRow);
    nrows = sh.nrows
    temstr = "";
    temstr += dataName + "= {"
    keyid = title[0];  # 第一个默认为关键字
    
    for i in range(noReadRow,nrows):
        # for j in range(0,nrows):
        strline = ""
        for keys in title:
            try:
                try:
                    j = maptitle[keys];
                except:
                    TestPrint("%s,%s表没有这个关键字:%s" % (fname, sheetName, keys))
                    raise 
                tems = GetCellValue(sh,i,j)
                if keys == keyid:
                    try:
                        strline = "\n%d:[" % int(tems); 
                    except:
                        TestPrint("%d行的数据异常" % (i + 1))
                        raise
                elif keys in string:
                    strline += "\'" + str(tems) + '\','
                elif keys in tuples:
                    tems = GetEvalStr(tems);
                    strline += tems + ','
                else:
                    strline += "%d" % int(tems) + ',';
            except:
                TestPrint("%s,%s,:%s,%d行出问题" % (fname, sheetName, keys, i + 1))
                raise 
        temstr += strline + '],'
    temstr += '\n}'
    return temstr

def MakeDir(name):
    p1 = name.rfind('/');
    path_name = name[:p1];
    try:
        os.makedirs(path_name);
    except:
        pass
    return 

def PubMakeMoreFile(data, title, string, tuples, floats, module1, module2, strClassNameFlag="", outFileNameFlag="", pathoutadd=""):
    ImportHeadFile = "import %s.%s\n" % (module1, module2)
    ClassName = "local _self={}\nfunction _self.create(self)\n\tif not self then self=C%s" % (module2) + "%s() end\n"
    OutFileName = "%s" % (module1)
    OutMoudleName = "%s%smodule" % (module1, outFileNameFlag)
    PathOut = "%s%s/%s/" % (pathoutadd, module1, module2)  # 注意是最后面是有/号
    MakeMoreFile(data, PathOut , title, string, tuples,floats, ImportHeadFile, ClassName, OutFileName, OutMoudleName, strClassNameFlag);
    return 

def MakeMoreFile(data, tempathout, title, string, tuples,floats, ImportHeadFile, ClassName, OutFileName, OutModuleName, strClassNameFlag=""):
    HeadBody = ""
    #HeadBody += ImportHeadFile
    for nid, temdata in data.items():
        if strClassNameFlag:
            if strClassNameFlag in string:
                tembody = ClassName % ("_" + temdata[strClassNameFlag]);
            else:
                tembody = ClassName % ("_" + str(int(temdata[strClassNameFlag])));
                
        else:
            tembody = ClassName % strClassNameFlag;
        body = tembody;
        for keys in title:
            try:
                tems = temdata[keys];
            except:
                TestPrint( "No This Data", "(id:", nid, "title:", keys,")\n", temdata )
                raise 
            try:
                if keys in string:
                    body += "\tself.m_%s =\'%s\'\n" % (keys, tems)
                elif keys in tuples:
                    tems = GetEvalStr(tems,True);
                    body += "\tself.m_%s = %s\n" % (keys, tems)
                elif keys in floats:
                    body += "\tself.m_%s = %f\n" % (keys, tems)
                else:
                    body += "\tself.m_%s = %d\n" % (keys, int(tems))
            except:
                TestPrint("数据出错", "(id:", nid, "列:", keys, ")\n", "出错值:%s" % tems, temdata)
                raise
        
        outfilename = tempathout + OutFileName + str(nid) + '.lua'
        MakeData2File(body, outfilename,AddFlag2 = "sysytem_data_start",AddFlag3 = "sysytem_data_end", AddHead=HeadBody) 
        body = "\treturn self end\nreturn _self" 
        MakeData2File(body, outfilename, AddFlag2 = "sysytem_auto_file_return_self_start",AddFlag3 = "sysytem_auto_file_return_self_end") 
        
    def OuputModuel(data, tempathout, OutFileName, OutModuleName): 
        # 输入到Moudel上
        temmoudle = tempathout.replace('/', '.') + OutFileName
        p1 = tempathout.rfind('/');
        outfilename = tempathout[:p1 + 1] + '../' + OutModuleName + '.lua';
        HeadBody = '''g_%s = {}\n''' % ( OutModuleName)
        body = ""
        #g_itemmodule[100] = "item.itemnormal.item100"
        for nid, temdata in data.items():
            tem = "%s%d" % (temmoudle, nid);
            #body += "import %s\n" % tem
            body += "g_%s[%d] = \"%s\"\n" % (OutModuleName, nid, tem)
        MakeData2File(body, outfilename, temmoudle, temmoudle , HeadBody)
    OuputModuel(data, tempathout, OutFileName, OutModuleName);
    return


def MakeData2File(body,pathout,AddFlag2 = "",AddFlag3 = "",AddHead = ""):
    pathout = g_PathOut + pathout
    MakeDir(pathout);    #
    head = "--# coding:%s\n" % g_encode + AddHead
    Flag1 = "--# 以上系统生成,请忽修改哦!"
    Flag2 = "--# 以下系统导表数据生成,请忽手动修改-" + AddFlag2
    Flag3 = "--# 以上系统导表数据生成,请忽手动修改-" + AddFlag3
    strtem = "";
    try:
        f = open(pathout,'r+');
        txt = f.read();
        p1 = txt.find(Flag1);
        p2 = txt.find(Flag2);
        p3 = txt.find(Flag3);
        if(p1 < 0):
            strtem += head + Flag1 + '\n';
            strtem += txt[p1:p2];
        else:
            strtem += txt[:p2];
        if p2 < 0:
            strtem += "\n"
        strtem += Flag2 + '\n';
        strtem += body
        if p3 < 0:
            strtem += '\n' + Flag3 ;
        strtem += '\n' + txt[p3:];
        f.close();
    except:
        strtem = head + Flag1 + '\n';
        strtem += Flag2 + '\n';
        strtem += body
        strtem += '\n' + Flag3 + '\n';
    f = open(pathout,'w+');
    f.write(strtem);
    f.close();
    return

def LuaMakeRequirHead(dataname):
    strtem = 'require "data.%s"' % dataname
    path = "data/data_head.lua"
    MakeData2File(strtem,path,dataname,dataname)
    return

def ReadData2MapList(fname,sheetName,title,string,tuples,dataName,noReadRow = 2):
    sh,maptitle,subtitle = GetSheetInfo(fname,sheetName,title,noReadRow);
    nrows = sh.nrows
    temstr = "";
    temstr += dataName + "= {"
    keyid = title[0];  # 第一个默认为关键字
    bAddSub = False;
    for i in range(noReadRow,nrows):
        # for j in range(0,nrows):
        strline = ""
        for keys in title:
            try:
                if type(keys) == tuple or  type(keys) == list:  # 子集
                    if not bAddSub:
                        strline += "["
                        bAddSub = True;
                    strline += "["
                    for keys in subtitle:
                        try:
                            j = maptitle[keys];
                        except:
                            TestPrint("%s,%s表没有这个关键字:%s" % (fname, sheetName, keys))
                            raise 
                        tems = GetCellValue(sh,i,j)
                        if keys in string:
                            strline += "\'" + tems + '\','
                        elif keys in tuples:
                            tems = GetEvalStr(tems);
                            strline += tems + ','
                        else:
                            strline += "%d" % int(tems) + ',';
                    strline += "],\n"
                    continue;
                    
                try:
                    j = maptitle[keys];
                except:
                    TestPrint("%s,%s表没有这个关键字:%s" % (fname, sheetName, keys))
                    raise 
                tems = GetCellValue(sh,i,j)
                if tems == "":
                    continue;
                if keys == keyid:
                    if bAddSub:
                        bAddSub = False;
                        strline += ']],';
                    try:
                        strline += "\n%d:[" % int(tems); 
                    except:
                        TestPrint("%d行的数据异常" % (i + 1))
                        raise
                elif keys in string:
                    strline += "\'" + str(tems) + '\','
                elif keys in tuples:
                    tems = GetEvalStr(tems);
                    strline += tems + ','
                else:
                    strline += "%d" % int(tems) + ',';
            except:
                TestPrint("%s,%s,:%s,%d行出问题" % (fname, sheetName, keys, i + 1))
                raise 
        if bAddSub:
            temstr += strline 
        else:
            temstr += strline + '],'
    if bAddSub:
        temstr += ']],';
    temstr += '\n}'
    return temstr


def ReadTestMapMapMap(fname,sheetName,title,string,tuples,dataName,noReadRow = 2):
    sh,maptitle,subtitle = GetSheetInfo(fname,sheetName,title,noReadRow);
    nrows = sh.nrows
    temstr = "";
    temstr += dataName + "= {"
    global  g_nCen;
    g_nCen = 0
    for i in range(noReadRow,nrows):
        def GetTitleStr(temtitle,ncen):
            global  g_nCen;
            strline = ""
            for ncur,keys in enumerate(temtitle):
                if (type(keys) == tuple or  type(keys) == list):  # 子集
                    strline += GetTitleStr(keys,ncen + 1);
                else:
                    try:
                        try:
                            j = maptitle[keys];
                        except:
                            TestPrint("%s,%s表没有这个关键字:%s" % (fname, sheetName, keys))
                            raise 
                        tems = GetCellValue(sh,i,j)
                        if  tems == "":
                            if g_nCen != ncen:
                                continue;
                            else:
                                raise
                        if ncur == 0:
                            try:
                                if g_nCen < ncen :
                                    strline += "\n{"
                                if g_nCen > ncen:
                                    strline += (g_nCen - ncen) * "\n}],"
                                g_nCen = ncen
                                
                                strline += "\n%d:[" % int(tems); 
                            except:
                                TestPrint("%d行的数据异常" % (i + 1))
                                raise
                        elif keys in string:
                            strline += "\'" + str(tems) + '\','
                        elif keys in tuples:
                            tems = GetEvalStr(tems);
                            strline += tems + ','
                        else:
                            strline += "%d" % int(tems) + ',';
                    except:
                        TestPrint("%s,%s,:%s,%d行出问题" % (fname, sheetName, keys, i + 1))
                        raise 
                    if ncur == len(temtitle) - 1:
                        strline += '],'
            return strline 
        temstr += GetTitleStr(title,0)
    temstr += g_nCen * "\n}]"
    temstr += '\n}';
    return temstr    

# #数据以Dict形式存并且Tile为读的关键字
def ReadTitleDict(fname, sheetName, title, string, tuples,floats, dataName, noReadRow=2):
    return ReadTitle2Dict(fname, sheetName, title, string, tuples, floats,dataName, noReadRow)

def ReadTitle2Dict(fname, sheetName, title, string, tuples,floats, dataName, noReadRow=2):
    sh, maptitle, subtitle = GetSheetInfo(fname, sheetName, title, noReadRow);
    nrows = sh.nrows
    temstr = "";
    temstr += dataName + "= {"
    keyid = title[0];  # 第一个默认为关键字
    #TestPrint("--maptitle",maptitle)
    for i in range(noReadRow, nrows):
        strline = ""
        for keys in title:
            try:
                try:
                    j = maptitle[keys];
                except:
                    TestPrint( "%s,%s表没有这个关键字:%s\n" % (fname, sheetName, keys))
                    raise 
                tems = GetCellValue(sh, i, j)
                temkey = "\'%s\':" % keys
                strline += temkey;
                if keys == keyid:
                    try:
                        strline = SetKeysStr(keys,tems,string)  #这种方法是强制识别
                        # if keys in string: 
                        #      strline = "\n \'%s\':{" % tems; 
                        # else:
                        #     strline = "\n%d:{" % int(tems);
                    except:
                        TestPrint( "%d行的数据异常\n" % (i + 1))
                        raise
                elif keys in string:
                    strline += "\'" + str(tems) + '\',' 
                elif keys in tuples:
                    tems = GetEvalStr(tems);
                    strline += tems + ','
                elif keys in floats:
                    strline += "%f" % (tems) + ',';
                else:
                    strline += "%d" % int(tems) + ',';
            except:
                TestPrint( "%s,%s,:%s,%d行出问题\n" % (fname, sheetName, keys, i + 1))
                raise 
        temstr += strline + '},'
    temstr += '\n}'
    return temstr

# #数据以Dict形式存并且Tile为读的关键字
def ReadTitleDictList(fname, sheetName, title, string, tuples,floats, dataName, noReadRow=2):
    sh, maptitle, subtitle = GetSheetInfo(fname, sheetName, title, noReadRow);
    nrows = sh.nrows
    temstr = "";
    temstr += dataName + "= {"
    keyid = title[0];  # 第一个默认为关键字
    bAddSub = False;
    for i in range(noReadRow, nrows):
        strline = ""
        for keys in title:
            try:
                if type(keys) == tuple or  type(keys) == list:  # 子集
                    if not bAddSub:
                        temkey = "\'%s\':" % keys[0]
                        strline += temkey;
                        strline += "["
                        bAddSub = True;
                    strline += "{"
                    for keys in subtitle:
                        try:
                            j = maptitle[keys];
                        except:
                            TestPrint( "%s,%s表没有这个关键字:%s\n" % (fname, sheetName, keys))
                            raise 
                        temkey = "\'%s\':" % keys
                        strline += temkey;
                        tems = GetCellValue(sh, i, j)
                        if keys in string:
                            strline += "\'" + tems + '\','
                        elif keys in tuples:
                            tems = GetEvalStr(tems);
                            strline += tems + ','
                        elif keys in floats:
                            strline += "%f" % (tems) + ',';
                        else:
                            strline += "%d" % int(tems) + ',';
                    strline += "},\n"
                    continue;
                    
                try:
                    j = maptitle[keys];
                except:
                    TestPrint( "%s,%s表没有这个关键字:%s\n" % (fname, sheetName, keys))
                    raise 
                tems = GetCellValue(sh, i, j)
                if tems == "":
                    continue;
                temkey = "\'%s\':" % keys
                if keys == keyid:
                    if bAddSub:
                        bAddSub = False;
                        strline += ']},';
                    try:
                        #strline += "\n%d:{" % int(tems); 
                        strline += SetKeysStr(keys,tems,string)
                    except:
                        TestPrint( "%d行的数据异常\n" % (i + 1))
                        raise
                elif keys in string:
                    strline += temkey;
                    strline += "\'" + str(tems) + '\','
                elif keys in tuples:
                    strline += temkey;
                    tems = GetEvalStr(tems);
                    strline += tems + ','
                elif keys in floats:
                    strline += temkey;
                    strline += "%f" % (tems) + ',';
                else:
                    strline += temkey;
                    strline += "%d" % int(tems) + ',';
            except:
                TestPrint( "%s,%s,:%s,%d行出问题\n" % (fname, sheetName, keys, i + 1))
                raise 
        if bAddSub:
            temstr += strline 
        else:
            temstr += strline + '},'
    if bAddSub:
        temstr += ']},';
    temstr += '\n}'
    return temstr
# #数据以Dict形式存并且Tile为读的关键字
def ReadTitleDictDictDict(fname, sheetName, title, string, tuples,floats, dataName, noReadRow=2):
    sh, maptitle, subtitle = GetSheetInfo(fname, sheetName, title, noReadRow);
    nrows = sh.nrows
    temstr = "";
    temstr += dataName + "= {"
    bAddSub = False;
    global  g_nCen;
    g_nCen = 0
    for i in range(noReadRow, nrows):
        def GetTitleStr(temtitle, ncen):
            global  g_nCen;
            strline = ""
            for ncur, keys in enumerate(temtitle):
                if (type(keys) == tuple or  type(keys) == list):  # 子集
                    strline += GetTitleStr(keys, ncen + 1);
                else:
                    try:
                        try:
                            j = maptitle[keys];
                        except:
                            TestPrint( "%s,%s表没有这个关键字:%s\n" % (fname, sheetName, keys))
                            raise 
                        tems = GetCellValue(sh, i, j)
                        if tems == "":
                            continue;
                        temkey = "\'%s\':" % keys
                        if ncur == 0:
                            try:
                                if g_nCen < ncen :
                                    strline += temkey;
                                    strline += "\n{"
                                if g_nCen > ncen:
                                    strline += (g_nCen - ncen) * "\n}},"
                                g_nCen = ncen
                                
                                #strline += "\n%d:{" % int(tems); 
                                strline += SetKeysStr(keys,tems,string)
                            except:
                                TestPrint( "%d行的数据异常\n" % (i + 1))
                                raise
                        elif keys in string:
                            strline += temkey;
                            strline += "\'" + str(tems) + '\','
                        elif keys in tuples:
                            strline += temkey;
                            tems = GetEvalStr(tems);
                            strline += tems + ','
                        elif keys in floats:
                            strline += temkey;
                            strline += "%f" % (tems) + ',';
                        else:
                            strline += temkey;
                            strline += "%d" % int(tems) + ',';
                    except:
                        TestPrint( "%s,%s,:%s,%d行出问题\n" % (fname, sheetName, keys, i + 1))
                        raise 
                    if ncur == len(temtitle) - 1:
                        strline += '},'
            return strline 
        temstr += GetTitleStr(title, 0)
    temstr += g_nCen * "\n}}"
    temstr += '\n}';
    return temstr    
    
    
    
    
