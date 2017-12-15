import os
import sys
import base64
import hashlib
import subprocess 
import time
import threading
import re
import sqlite3
import queue
import math
import traceback
import appscript


try:
    from collections import OrderedDict
    print("use OrderedDict")
except:
    print("no OrderedDict, use dict!")
    OrderedDict = dict

art_path = "/Users/moqikaka_zb/Documents/Projects/NewFreshMan/Client/Client/res/ui"
record_path = "/Users/moqikaka_zb/Documents/Projects/NewFreshMan/Client/Client/res/ui_old/缺失的图_赵.txt"
old_art_path ="/Users/moqikaka_zb/Documents/Projects/NewFreshMan/Client/Client/res/ui_old/ui"
spare_path = "/Users/moqikaka_zb/Documents/Projects/NewFreshMan/Client/Client/res/ui_old/zb/ui"


file_path = ["/Users/moqikaka_zb/Documents/Projects/NewFreshMan/Client/Client/src/copy",
             "/Users/moqikaka_zb/Documents/Projects/NewFreshMan/Client/Client/src/more",
             ]


# 匹配 TR("中文-字符串"
reTR = re.compile(r'TR\s*\(\s*\"(.+?)(?<!\\)\"')
reFindAllTR = reTR.findall

# 删除注释
reSubComment = re.compile(r'^(--.*)').sub

def readText(_file_path):
    fileExitDic = OrderedDict()
    f = open(_file_path, "r+")
    if not f:
        print('cannot open file: %s' % (lua))
        return []
    # 读取文件
    lines = f.readlines()
    dirname, filename = os.path.split(_file_path)
    # print(dirname)
    # print(filename)
    # 逐行匹配  TR("xx")
    lineNum = 0
    errorNums = []
    for l in lines:
        lineNum += 1
        c = reMatchMissing(l)
        if c:
            for m in c: 
                tmpStr = str.format("%s,%d,%s" % (m,lineNum,filename))
                fileExitDic[m] = tmpStr
                # print(m)
    f.close()
    return fileExitDic

def reMatchMissing(line, isGuide = False):
    line = re.compile(r'--.*').sub('', line)
    line = re.compile(r'dump\s*\(.*?\)').sub('', line)
    line = re.compile(r'print\s*\(.*?\)').sub('', line)

    if isGuide:
        line = re.compile(r'tag\s*=\s*\".*?(?<!\\)\"').sub('', line)
    t = re.findall(r'\"ui/(.+?)(?<!\\)\"',line)
    if t:
        return t
    t2 = re.findall(r'\"ui_old/zb/ui/(.+?)(?<!\\)\"',line)
    if t2:
        return t2
    return None

def getAllMatch():
    allInfo = OrderedDict()
    for fp in file_path:
        fc  = os.walk(fp)
        for dir_path,subpaths,files in fc:
            for f in files:
                if not f.startswith('.'):
                    # 跳过Config目录
                    if os.path.join(dir_path, f).find('Config/') >= 0:
                        continue
                    if f == "Language.lua" or f == "GodLayer.lua":
                        continue
                    if not f.endswith(".lua"):
                        continue
                    trs = readText(os.path.join(dir_path, f))    # 获取当前文件字中文符串
                    allInfo = dict(allInfo,**trs)

    return allInfo
        

    
def main():
    # str1 = "Finder"
    # str1 = "Sublime Text 2"
    # str1 = "Microsoft Word"
    # str1 = "QQ"
    str1 = "iTunes"
    ituns = appscript.app(str1)
    print(ituns.help("-o"))
    # ituns.open(file_path[0])
    #print(help(ituns))
    # print(sys.argv[1])
    # c = os.walk(art_path)
    # uiDic = OrderedDict()
    # tmpexitDic = getAllMatch()

    # for dir_path,subpaths,files in c:
    #     for f in files:
    #         if not f.startswith('.'):
    #             uiDic[f] = f
 
    # exitDic = OrderedDict()
    # for i in tmpexitDic:
    #     if uiDic.get(i) == None:
    #         exitDic[i] = tmpexitDic[i]
            
    # if os.path.exists(record_path):
    #         os.system("rm %s" % record_path)

    # oldpath = os.getcwd()
    # os.chdir("/Users/moqikaka_zb/Documents/Projects/NewFreshMan/Client/Client/res/ui_old/")
    # f = open("缺失的图_赵.txt","w")
    # os.chdir(oldpath)

    # #未找到内容
    # for x in exitDic:
    #     a = str.split(exitDic[x],",")
    #     lineStr = str.format("资源名:%-25s文件名:%-30s行号:%-5s\n" % (a[0],a[2],a[1]))
    #     f.write(lineStr)
    #     # print(str.format("资源名:%-25s文件名:%-30s行号:%-5s" % (a[0],a[2],a[1])))

    # f.close()


    # if not os.path.exists(spare_path):
    #         os.makedirs(spare_path)

    # oc = os.walk(old_art_path)
    
    # oldDic = OrderedDict()
    # for dir_path,subpaths,files in oc:
    #     for f in files:
    #         oldDic[f] = f
    
    # for x in exitDic:
    #     a = str.split(exitDic[x],",")
    #     if oldDic.get(a[0]):
    #         os.system("cp %s/%s %s/%s" % (old_art_path,a[0],spare_path,a[0]))
            
    #     else:
    #         print(str.format("未找到对应资源名:%-25s文件名:%-30s行号:%-5s" % (a[0],a[2],a[1])))


    # zbc = os.walk(spare_path)
    # zbDic = OrderedDict()

    # for dir_path,subpaths,files in zbc:
    #     for f in files:
    #         if uiDic.get(f):
    #             print("清除已存在图片:%s" % f)
    #             os.system("rm %s/%s" % (spare_path,f))


    

if __name__ == '__main__':
    main()