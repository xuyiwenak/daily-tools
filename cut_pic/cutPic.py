# coding=utf-8

from PIL import Image
import json, sys, os

def loadFileConfig(configPath):
    """
    读取资源分片打包管理配置的路径, 默认为本机目录的sourManConfig.json
    :param configPath:读取打包配置的路径
    :return:
    """
    if not os.path.exists(configPath):
        print configPath,"      <-----------配置文件加载失败！请确认配置路径！"
        return
    with open(configPath, 'r') as f:
        try:
            config = json.loads(f.read())
        except:
            print configPath, "      <-----------配置加载失败！请确认配置内容！"
            sys.exit()
        return config

def dividePic(imageName, outName, position, folderDir):
    """
    :param imageName: 
    :return: 
    """
    im = Image.open(imageName, "r")
    posList = []
    posList.append(position.get("x"))
    posList.append(position.get("y"))
    posList.append(position.get("x")+ position.get("w"))
    posList.append(position.get("y") + position.get("h"))
    box = tuple(posList)
    region = im.crop(box)
    extendWith = imageName.split(".")[1]
    if not os.path.exists(os.getcwd() + folderDir):
        os.makedirs(os.getcwd() + folderDir)
    region.save(os.getcwd()+folderDir+outName + "." + extendWith, extendWith)

def picHandler():
    """
    
    :return: 
    """
    curPath = os.getcwd()
    folderDir = "/sliceImg/"
    if not os.path.exists(os.getcwd() + folderDir):
        os.makedirs(os.getcwd() + folderDir)
    fileList = os.listdir(curPath)
    for file in fileList:
        if file.endswith(".png") or file.endswith(".jpg"):
            filePrefix=file.split(".")[0]
            jsonConfFile = filePrefix + ".json"
            print jsonConfFile
            confDict = loadFileConfig(jsonConfFile)
            if not confDict:
                continue
            sliceDict = confDict.get("frames")
            for outName, position in sliceDict.items():
                dividePic(file, outName, position, folderDir)

if __name__ == '__main__':
    picHandler()
