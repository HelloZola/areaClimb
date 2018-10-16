# -*- coding: UTF-8 -*-
import thread
import time
import datetime
import sys
from com.vi.climb.NormalToClimbData import *

def threadToClimb(province):
    
    starttime = datetime.datetime.now()##开始时间
    localPath = "G:/Tem/"
    baseUrl = "http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2015/"
    name = province.get("name")
    code = province.get("code")
    print "开始拉取省份数据，省份："+name
    fo = open("G:\\Tem\\" + name.decode('UTF-8').encode('GBK')  + ".csv", "w")
    cityInfos = climbCityData(province, baseUrl)
    if not cityInfos is None:
        saveCitys(fo, cityInfos)
        print "省份：" + province.get("name") + "|城市数目：", len(cityInfos)
        for cityInfo in cityInfos:
            countys = climbCountyData(cityInfo, baseUrl)
            countyBaseUrl = baseUrl + (province.get("address").split("."))[0] + "/"
            if not countys is None:
                saveCountys(fo, countys)
                print "省份：" + province.get("name") + "|城市：" + cityInfo.get("name") + "|城区数目：", len(countys)
                for county in countys:
                    towers = climbTowerData(county, countyBaseUrl)
                    towerBaseUrl = countyBaseUrl + (((county.get("address").split("."))[0]).split("/"))[0] + "/"
                    if not towers is None:
                        saveTowers(fo, towers)  
                        print "省份：" + province.get("name") + "|城市：" + cityInfo.get("name") + "|城区：" + county.get("name") + "|城镇数目：", len(towers)
                        for tower in towers:
                            villagetrs = climbVillagetrsData(tower, towerBaseUrl)
                            if not villagetrs is None:
                                saveVillagetrs(fo, villagetrs)
                                print "省份：" + province.get("name") + "|城市：" + cityInfo.get("name") + "|城区：" + county.get("name") + "|城镇：" + tower.get("name") + "|村居委会街道办数目：", len(villagetrs)
    endtime = datetime.datetime.now()
    print "拉取省份数据完成，"+"用时（s）：",(endtime - starttime).seconds," |省份：",name
    fo.close()
    

def run():
    starttime = datetime.datetime.now()  # #开始时间
    url = "http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2015/index.html";
    baseUrl = "http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2015/"
    fo = open("G:\\Tem\\provinces.csv", "w")
    html = getHtml(url)
    provinces = getProvinceInfo(html)
    saveProvinces(fo, provinces)
    fo.close() 
    for pro in provinces:
        thread.start_new_thread(threadToClimb, (pro,))     
    time.sleep(30)
       
##开始拉取
run()
