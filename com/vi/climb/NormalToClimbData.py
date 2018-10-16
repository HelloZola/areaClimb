# coding=utf-8
import os, sys
import urllib
import urllib2
import datetime
import time
from com.vi.utils.CharUtil import *

def getHtml(url):
#     header = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:48.0) Gecko/20100101 Firefox/48.0"}
    header = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    req = urllib2.Request(url=url, headers=header)
    result = urllib2.urlopen(req)  # 发起GET http服务
    html = result.read()  # 把结果通过.read()函数读取出来
    html = unicode(html, "gbk").encode("utf8")
    return html

def getCitys(provinceInfo,baseUrl):
    
    address = provinceInfo.get("address")
    url = baseUrl+address;
    html = getHtml(url)
    cityInfos = getCityInfo(provinceInfo,html)
    return cityInfos


def getCountys(cityInfo,baseUrl):
    address = cityInfo.get("address")
    if address.strip()=='':
        print "地址链接为空：",cityInfo
        pass
    else:
        url = baseUrl+address;
        html = getHtml(url)
        countys = getCountyInfo(cityInfo,html)
        return countys

def getTowers(countyInfo,baseUrl):
    address = countyInfo.get("address")
    if address.strip()=='':
        print "地址链接为空：",countyInfo
        pass
    else:
        url = baseUrl+address;
        html = getHtml(url)
        towers = getTowerInfo(countyInfo,html)
        return towers
    
def getVillagetrs(towerInfo,baseUrl):
    address = towerInfo.get("address")
    if address.strip()=='':
        print "地址链接为空：",towerInfo
        pass
    else:
        url = baseUrl+address;
        html = getHtml(url)
        towers = getVillagetrsInfo(towerInfo,html)
        return towers

# 编码、上级编码、名称、级别
def saveProvinces(file,provinces):
    for province in provinces:
        file.write(province.get("code")+","+"-1"+","+province.get("name")+","+province.get("code")+","+"1"+"\n")
        
# 编码、上级编码、名称、级别
def saveCitys(file,citys):
    for city in citys:
        file.write(city.get("code")+","+city.get("lastCode")+","+city.get("name")+","+city.get("code")+","+"2"+"\n")
        
# 编码、上级编码、名称、级别
def saveCountys(file,countys):
    for county in countys:
        file.write(county.get("code")+","+county.get("lastCode")+","+county.get("name")+","+county.get("code")+","+"3"+"\n")
        
# 编码、上级编码、名称、级别       
def saveTowers(file,towers):
    for tower in towers:
        file.write(tower.get("code")+","+tower.get("lastCode")+","+tower.get("name")+","+tower.get("code")+","+"4"+"\n")
        
# 编码、上级编码、名称、级别        
def saveVillagetrs(file,villagetrs):
    for villagetr in villagetrs:
        file.write(villagetr.get("code")+","+villagetr.get("lastCode")+","+villagetr.get("name")+","+villagetr.get("code")+","+"5"+"\n")



def climbCityData(pro,baseUrl):
    
    try:
        cityInfos = getCitys(pro,baseUrl)
    except Exception,err:
        print err
        print "查找省份-城市数据发生异常，省份：",pro.get("name")
        print "休息10秒后再次查找"
        print "......"
        time.sleep(10)
        print "开始再次查找"
        return climbCityData(pro,baseUrl)
    else:
        pass
        return cityInfos
    
def climbCountyData(cityInfo,baseUrl):
    
    try:
        countys = getCountys(cityInfo,baseUrl)
    except Exception,err:
        print err
        print "查找城市-城区数据发生异常，城市：",cityInfo.get("name")
        print "休息10秒后再次查找"
        print "......"
        time.sleep(10)
        print "开始再次查找"
        return climbCountyData(cityInfo,baseUrl)
    else:
        pass
        return countys
          
def climbTowerData(county,baseUrl):
    
    try:
        towerInfos = getTowers(county, baseUrl)
    except Exception,err:
        print err
        print "查找城区-城镇数据发生异常，城区：",county.get("name")
        print "休息10秒后再次查找"
        print "......"
        time.sleep(10)
        print "开始再次查找"
        return climbTowerData(county,baseUrl)
    else:
        pass
        return towerInfos


def climbVillagetrsData(tower,baseUrl):
    
    try:
        villagetrs = getVillagetrs(tower, baseUrl)
    except Exception,err:
        print err
        print "查找城镇-乡村数据发生异常，城镇：",tower.get("name")
        print "休息10秒后再次查找"
        print "......"
        time.sleep(10)
        print "开始再次查找"
        return climbVillagetrsData(tower,baseUrl)
    else:
        return villagetrs


# 1.获取地域内容  - 休息重试模式
def startX():
    
    starttime = datetime.datetime.now()##开始时间
    url = "http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2015/index.html";
    baseUrl = "http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2015/"
    fo = open("G:\\Tem\\area_citys.csv", "w")
    html = getHtml(url)
    provinces = getProvinceInfo(html)
    saveProvinces(fo,provinces)
    for pro in provinces:
        cityInfos = climbCityData(pro,baseUrl)
        if not cityInfos is None:
            saveCitys(fo,cityInfos)
            print "省份："+pro.get("name")+"|城市数目：",len(cityInfos)
            for cityInfo in cityInfos:
                countys = climbCountyData(cityInfo,baseUrl)
                countyBaseUrl = baseUrl+(pro.get("address").split("."))[0]+"/"
                if not countys is None:
                    saveCountys(fo,countys)
                    print "省份："+pro.get("name")+"|城市："+cityInfo.get("name")+"|城区数目：",len(countys)
                    for county in countys:
                        towers = climbTowerData(county,countyBaseUrl)
                        towerBaseUrl = countyBaseUrl+(((county.get("address").split("."))[0]).split("/"))[0]+"/"
                        if not towers is None:
                            saveTowers(fo,towers)  
                            print "省份："+pro.get("name")+"|城市："+cityInfo.get("name")+"|城区："+county.get("name")+"|城镇数目：",len(towers)
                            for tower in towers:
                                villagetrs = climbVillagetrsData(tower,towerBaseUrl)
                                if not villagetrs is None:
                                    saveVillagetrs(fo,villagetrs)
                                    print "省份："+pro.get("name")+"|城市："+cityInfo.get("name")+"|城区："+county.get("name")+"|城镇："+tower.get("name")+"|村居委会街道办数目：",len(villagetrs)
    fo.close()
    endtime = datetime.datetime.now()
    print "用时（s）：",(endtime - starttime).seconds                                 
                                    
                                    
# 1.获取地域内容  - 简单模式（中途可能会由于频繁拉取而报错）
def start():
    
    starttime = datetime.datetime.now()##开始时间
    url = "http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2015/index.html";
    baseUrl = "http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2015/"
    fo = open("G:\\Tem\\area.csv", "w")
    html = getHtml(url)
    provinces = getProvinceInfo(html)
    
    saveProvinces(fo,provinces)
    for pro in provinces:
        cityInfos = getCitys(pro,baseUrl)
        if not cityInfos is None:
            saveCitys(fo,cityInfos)
            print "省份："+pro.get("name")+"|城市数目：",len(cityInfos)
            for cityInfo in cityInfos:
                countys = getCountys(cityInfo,baseUrl)
                countyBaseUrl = baseUrl+(pro.get("address").split("."))[0]+"/"
                if not countys is None:
                    saveCountys(fo,countys)
                    print "省份："+pro.get("name")+"|城市："+cityInfo.get("name")+"|城区数目：",len(countys)
                    for county in countys:
                        towers = getTowers(county,countyBaseUrl)
                        towerBaseUrl = countyBaseUrl+(((county.get("address").split("."))[0]).split("/"))[0]+"/"
                        if not towers is None:
                            saveTowers(fo,towers)
                            print "省份："+pro.get("name")+"|城市："+cityInfo.get("name")+"|城区："+county.get("name")+"|城镇数目：",len(towers)
                            for tower in towers:
                                villagetrs = getVillagetrs(tower,towerBaseUrl)
                                if not villagetrs is None:
                                    saveVillagetrs(fo,villagetrs)
                                    print "省份："+pro.get("name")+"|城市："+cityInfo.get("name")+"|城区："+county.get("name")+"|城镇："+tower.get("name")+"|村居委会街道办数目：",len(villagetrs)
    fo.close()                               
    endtime = datetime.datetime.now()
    print "用时（s）：",(endtime - starttime).seconds
    
##开始拉取                                                        
startX()

# countyInfo = {'name': "长安区", 'address': "01/130102.html", 'code': "130102000000", 'lastCode':"130000000000"}
# baseUrl = "http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2015/13/"
# Towntrs = getTowntrs(countyInfo, baseUrl)
# for towntr in Towntrs:
#     print towntr.get("lastCode")," ",towntr.get("code")," ",towntr.get("name")," ",towntr.get("address")


# tower = {'name': "长安区", 'address': "01/130102.html", 'code': "130102000000", 'lastCode':"130000000000"}
# baseUrl = "http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2015/13/"
# Towntrs = getTowntrs(tower, baseUrl)
# for towntr in Towntrs:
#     print towntr.get("lastCode")," ",towntr.get("code")," ",towntr.get("name")," ",towntr.get("address")


# tower = {'name': "沙面街道", 'address': "03/440103001.html", 'code': "440103001000", 'lastCode':"130000000000"}
# baseUrl = "http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2015/44/01/"
# Villagetrs = getVillagetrs(tower, baseUrl)
# for Villagetr in Villagetrs:
#     print Villagetr.get("lastCode")," ",Villagetr.get("code")," ",Villagetr.get("name")," ",Villagetr.get("address")," ",Villagetr.get("town&countryType")

