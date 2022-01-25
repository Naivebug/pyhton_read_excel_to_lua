#!/usr/bin/env python
# -*- encoding:utf8 -*-

from genericpath import exists
import sys, os, re
from tracemalloc import start
import slpp
import json


def main(dir):
	for filename in os.listdir(dir):
		filetype = filename[-6:]
		if filetype == ".proto":
			#f = open(dir + filename)
			print(dir + filename)
			os.system("protoc.exe -o %s.pb %s"%(dir +'outlua/' + filename[0:-6] ,dir  + filename))
			os.system("protoc.exe %s  --csharp_out=%s" %(dir  + filename,dir +'outcs/'))

if __name__ == "__main__":
	dir = "./" if len(sys.argv)<=1  else sys.argv[1]
	main(dir)

