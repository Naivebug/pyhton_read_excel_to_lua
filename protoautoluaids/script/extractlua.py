#!/usr/bin/env python
# -*- encoding:utf8 -*-

from genericpath import exists
import sys, os, re
from tracemalloc import start
import slpp
import json


def main(dir):
	startbaseid = 256+1;
	startid = 256;
	maxid = 65535;
	dc = {}
	dcids = {}
	if exists("protoidjs.json"):
		f = open("protoidjs.json","r+")
		buf = f.read()
		f.close()
		dcs = json.loads(buf)
		dc = dcs["name"]
		if dc:
			for k,v in dc.items():
				dcids[v] = k
				if v > startid : 
					startid = v 
				

	re_message = re.compile("message\s\w+")
	re_pack = re.compile("(package)(\s\w+)")
	ls2 = []
	bok = True
	newdc = {}
	newids = {}
	for filename in os.listdir(dir):
		filetype = filename[-6:]
		if filetype == ".proto":
			f = open(dir + filename)
			buf = f.read()
			f.close()
			ls = re_pack.findall(buf)
			protoname = ""
			if len(ls) > 0 :
				protoname = ls[0][1].strip() + "."
			ls = re_message.findall(buf)
			#
			for s in ls :
				name = s.replace("message", "").strip()
				if not name[0:3] in ["C2S","S2C","c2s","s2c"] :
					continue
				s2 = protoname + name # s.strip("message").strip() 
				if s2 in dc:
					newdc[s2] = dc[s2]
					newids[dc[s2]] = s2
					ls2.append(s2)
					#print("Warring:\n\t注意有协议重复了",s2)
				else:
					startid = startid + 1
					temid = startid
					for i in range(maxid - startbaseid):
						key = i + startbaseid
						if  key not in  dcids and  key not in newids : 
							temid = key 
							break;
					if startid >= maxid : print("warring:\n\t注意已超过了最大2字节的ID了")
					newdc[s2] = temid
					newids[temid] = s2
					ls2.append(s2)
					bok = True
	if bok: #有数据更新
		#write json
		savedc = {"name":newdc,"idnames":newids}
		tem = json.dumps(savedc,indent=True)
		f = open("protoidjs.json", "w")
		f.write(tem)
		f.close()
		#write lua
		tem ="return " + slpp.SLPP().encode(savedc,[","])
		f = open("protoids.lua", "w")
		f.write(tem)
		f.close()
		#out cs
		printCs(newdc)

def printCs(newdc):
	txt = """
using Google.Protobuf;
using System.Collections.Generic;
namespace protos
{
	class protoids
	{
		public delegate object Fn(byte[] data);
	"""
	txtend = "\t}\n}"
	#add idnames
	body = "\tpublic static Dictionary<int, string> idnames = new Dictionary<int, string>(){\n"
	body2 = "	\tpublic static Dictionary<string,int> nameids = new Dictionary<string, int>(){\n"
	body3 = "	\tpublic static Dictionary<int, Fn> ids = new Dictionary<int, Fn>(){\n"
	for name,id in newdc.items() : 
		body += "\t\t\t[%d] = \"%s\",\n"%(id,name)
		body2 += "\t\t\t[\"%s\"] = %d,\n"%(name,id)
		body3 += "\t\t\t[%d] = %s.Parser.ParseFrom,\n"%(id,name)
	#add nameids
	body += "\t\t};\n"
	body2 += "\t\t};\n"
	body3 +="\t\t};\n"
	text = txt + body + body2 + body3 + txtend
	f = open("protoidscs.cs", "w")
	f.write(text)
	f.close()
	
	


if __name__ == "__main__":
	dir = "./" if len(sys.argv)<=1  else sys.argv[1]
	main(dir)