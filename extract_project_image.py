#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import shutil
import json
import string

count = 0 
inputPath = raw_input("input path:")
outputPath = raw_input("output path:")
imageType = raw_input("全选择倍图类型  2x or 3x:")
# inputPath = "/Users/zhangyu/Desktop/work/code/CloudLearning_Online_English/CloudLearning_Online_English/XOLGrENGroupLearning"
# outputPath = "/Users/zhangyu/Desktop/testimage"
# imageType = '2x'

def create_dirs(dirsPath):
	if not os.path.exists(dirsPath):
		os.makedirs(dirsPath)
		print dirsPath + "------目录不存在，进行创建目录"

create_dirs(outputPath)
create_dirs(outputPath + os.sep + 'xcassets')

def from_imageset(path,output):
	if not os.path.isdir(path):
		print path + "不是一个.imageset后缀的文件夹 请检查"
		return

	jsonPath = path + os.sep + "Contents.json"
	if not os.path.isfile(jsonPath):
		print path + "不是文件 请检查"
		return

	dataFile = open(jsonPath,'r')
	jsonData = dataFile.read();
	jsonDic = json.loads(jsonData)
	imageArray = jsonDic.get('images')
	for imageDic in imageArray:
		global imageType
		if imageDic.get('scale') == imageType:
			if not imageDic.get('filename'):
				return
			fileName = imageDic.get('filename')
			filePath = path + os.sep + fileName
			if os.path.isfile(filePath):
				imageOutPutPath = output + os.sep + 'xcassets' + os.sep + fileName
				global count
				count = count + 1;
				if os.path.isfile(imageOutPutPath):
					imageOutPutPath = output + os.sep + 'xcassets' + os.sep + bytes(count) + '_' + fileName

				print "input path : " + path + "\noutput path :" + imageOutPutPath + "\n" * 2
    			shutil.copyfile(filePath,imageOutPutPath)


def picture_extraction(path,output,bundle = 'None'):
    if os.path.isdir(path):
    	if path.endswith('.imageset'):
    		from_imageset(path,output)
    		return
        for i in os.listdir(path):
        	if not i.startswith('.'):
        		next = path + os.sep + i
        		if i.endswith('.bundle'):
        			picture_extraction(next,output,i)
        		else:
        			picture_extraction(next,output,bundle)
    elif os.path.isfile(path):
    	global imageType
    	fileKey = imageType + '.png'
    	if path.endswith(fileKey):
    		global count
    		imageOutPutPath = ''
    		if bundle:
    			outputBundlePath = output + os.sep + bundle
    			create_dirs(outputBundlePath)
    			imageOutPutPath = outputBundlePath + os.sep + os.path.basename(path)
    			print imageOutPutPath
    		else:
    			imageOutPutPath = output + os.sep + os.path.basename(path)
    			print imageOutPutPath
    		
    		if os.path.isfile(imageOutPutPath):
    			# 有重名文件重名名
    			imageOutPutPath = output + os.sep + bytes(count) + '_' + os.path.basename(path)
    			pass
    		print "input path : " + path + "\noutput path :" + imageOutPutPath + "\n" * 2
    		count = count + 1
    		shutil.copyfile(path,imageOutPutPath)


picture_extraction(inputPath,outputPath)

print "已拷贝" + bytes(count) + "个" + imageType + "图"

