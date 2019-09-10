# coding=utf-8

import json, os, sys
import requests
import threading
import Queue, time

def loadFileConfig(configPath):
    """
    读取资源分片打包管理配置的路径, 默认为本机目录的sourManConfig.json
    :param configPath:读取打包配置的路径
    :return:
    """
    if not os.path.exists(configPath):
        print configPath,"      <-----------配置文件加载失败！请确认配置路径！"
        sys.exit()
    with open(configPath, 'r') as f:
        try:
            config = json.loads(f.read())
        except:
            print configPath, "      <-----------配置加载失败！请确认配置内容！"
            sys.exit()
        return config


def phraseJsonName(config, jsPath):
    """
    
    :param config: 
    :return: 
    """
    slotList = config.get("skins").get("slots")
    for slot in slotList:
        fileName = slot.get("name")
        if fileName == "layer":
            picName = "layer.jpg"
        else:
            picName = fileName + ".png"
        imageDir = jsPath + "images/"
        if not os.path.exists(os.getcwd() + imageDir):
            os.makedirs(os.getcwd()+ imageDir)
        foldUrl = "%s/%s" % (imageDir, picName)
        picUrl = urlPrefix + foldUrl
        download(picUrl, imageDir, picName)


def getJsonFileFromCDN(urlPrefix, jsPath):
    """
    
    :param cdnJsUrl: 
    :return: 
    """
    cdnJsUrl = urlPrefix + jsPath
    folderDir = jsPath + "images/"
    downloadFile = requests.get(cdnJsUrl + "level.json")
    if not os.path.exists(os.getcwd() + folderDir):
        os.makedirs(os.getcwd() + folderDir)
    with open(os.getcwd() + folderDir + "level.json", 'wb') as file:
        file.write(downloadFile.content)
    config = loadFileConfig(os.getcwd() + folderDir + "level.json")
    phraseJsonName(config, jsPath)


def download(url, folderDir, picName):
    """
    
    :param url: 
    :param fileName: 
    :return: 
    """
    # 切目录下载
    downloadFile=requests.get(url)
    with open(os.getcwd() + folderDir + picName, 'wb') as file:
        file.write(downloadFile.content)

def urlCombine(i):
    """
    
    :param fileName: 
    :return: 
    """
    urlPrefix = "https://cdnks.hn.shqi7.net/runtuzhaocha/gameres/"
    jsPath = "/maps/lv_%s/" % i

    getJsonFileFromCDN(urlPrefix, jsPath)

def asume(i, li):

    while(len(li)>0):
        for t in range(100):
            t += 1
        index = li.pop()
        urlCombine(index)

urlPrefix = "https://cdnks.hn.shqi7.net/runtuzhaocha/gameres/"
if __name__ == '__main__':
    li = range(1201, 2501)
    start = int(time.time() * 1000)
    ps = []
    for i in range(10):
        p = threading.Thread(target=asume, args=(i, li))
        p.start()
        ps.append(p)
    for p in ps:
        p.join()
    end = int(time.time() * 1000)
    asume = end - start
    print "asume: ", asume
