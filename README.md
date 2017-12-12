easy python read xml to lua data export to file
# -*- coding: utf-8 -*-

#create by NaiveBug^梁疯

为了方便大家,特意开源一个Excel导表工具.

------------
#1先先安装Python2.7~please install python2.7

#2python install xlrd (这步百度搜索自己解决)

#3点击script下build编译并导出excel表文件到excel/script目录下.

------------
**报错提示**

当导表Excel表配置错误时,并会有报错提示..提示哪个导表,哪行哪个字段会有问题,原因是什么

------------

导出模式支持多种~以后在完善例子..

暂时写了支持单文件模式和多文件模式

-------想修改自己路径配置-----

1修改_startme.py文件,修改ReadPathExcel文件路径和PathOut文件输出的路径..

-------想添加自己的新Excel导表如战斗表----

1添加战斗导表和新建文件make_war.py..并把make_hero.py里的模式拷贝过去,修改下表头tile即可,(ps:string代表字符串类型,tuples代表元组或字典类型,float
代码小数点类型)

2在init文件ls添加描述,按哪个数字键快迅导指定表,输入0就导所有的表..在下面加入执行导表的代码如技能加入(if input in [0,2]:#技能)这段代码..接着点build就能导出你想要的表,

函数解释:(可直接看代码搞定啦)

ReadTitle2Dict:读导表数据成Python类型

Change2LuaData:把Python数据转成Lua数据

MakeData2File:导出数据到文件

--多文件模式,适合技能等直接每个技能自动生成一个文件,方便写面象对象代码.可直接在导表里面写代码呢.

ReadMoreFile:读取多文件模式

PubMakeMoreFile:输出多文件模式

PS**Excel文件里的字段可随时剪切掉换位置而不需要通知程序,但是如果删除了或增加就需要通知程序对应去添加.

PS**我知道市面上挺多导表是直接自动导,不需要加Python文件,但是如果自己加个Python文件写的会能支持更加强大的功能.具体还有功能以后我有空在添加上来..具体有需要也可以轻松支持自动不需要添加Pyhton文件,而是把配置搞到导表去,但这个有需求就自己来弄

有何建议可以在里面评论或到Skynet群里@clear,云风大哥能力大做大贡献,我能力弱就做小贡献...



 
