# coding=utf-8
import re

# 从td元素中获取访问地址，适用：省、市
def getAddressFromTdEle(tdStr):
    
    addressArr = re.findall("[^'""]*html\s*[^'""]*", tdStr)
    if len(addressArr) > 0:
        return addressArr[0]
    else:
        return ''
    
# 从td元素中获取中文名称 适用：省
def getChinaNameFromTdEle(tdStr):
    
    chinaNameArr = re.match(r'.*<a\s*href.*>(.*)<br.*', tdStr)
    return chinaNameArr.group(1)

# 从td元素中获取中文名称 适用：市、区
def getChinaNameFromTdEle2(tdStr):
    
    arr = re.findall(".*<a\s*href.*>(.*)</a.*", tdStr)
    if len(arr) == 0:
        chinaNameArr = re.match(r'.*<td>(.*)</td>', tdStr)
        return chinaNameArr.group(1)
    else:
        chinaNameArr = re.match(r'.*<a\s*href.*>(.*)</a.*', tdStr)
        return chinaNameArr.group(1)

# 从td元素中获取中文名称 适用：市、区
def getCodeFromTdEle(tdStr):
    
    arr = re.findall(".*<a\s*href.*>(.*)</a.*", tdStr)
    if len(arr) == 0:
        codeArr = re.match(r'.*<td>(.*)</td>', tdStr)
        return codeArr.group(1)
    else:
        codeArr = re.match(r'.*<a\s*href.*>(.*)</a.*', tdStr)
        return codeArr.group(1)

# 根据正则表达式获取字符串 - 获取省份信息
def getProvinceInfo(Str):
    
    result = []
    arr = re.findall('<td><a(?:(?!td).)*</a></td>', Str)
    for ar in arr:
        name = getChinaNameFromTdEle(ar)
        address = getAddressFromTdEle(ar)
        code = (address.split("."))[0] + "0000000000"
        dict = {'name': name, 'address': address, 'code': code}
        result.append(dict)
    return result

# 根据正则表达式获取字符串 - 获取市信息
def getCityInfo(provinceInfo, Str):

    result = []
    trArr = re.findall('<tr\s*class=[\"\']citytr[\"\'](?:(?!tr).)*</tr>', Str)
    for trAr in trArr:
        tdArr = re.findall('<td><a(?:(?!td).)*</a></td>', trAr)
        name = getChinaNameFromTdEle2(tdArr[1])
        code = getCodeFromTdEle(tdArr[0])
        address = getAddressFromTdEle(tdArr[0])
        lastCode = provinceInfo.get("code")
        dict = {'name': name, 'address': address, 'code': code, 'lastCode':lastCode}
        result.append(dict)
    return result


# 根据正则表达式获取字符串 - 获取区信息
def getCountyInfo(cityInfo, Str):

    result = []
    trArr = re.findall('<tr\s*class=[\"\']countytr[\"\'](?:(?!tr).)*</tr>', Str)
    for trAr in trArr:
        tdArr = re.findall('<td>(?:(?!td).)*</td>', trAr)
        name = getChinaNameFromTdEle2(tdArr[1])
        address = getAddressFromTdEle(tdArr[0])
        code = getCodeFromTdEle(tdArr[0])
        lastCode = cityInfo.get("code")
        dict = {'name': name, 'address': address, 'code': code, 'lastCode':lastCode}
        result.append(dict)
    return result


def getTownAndcountryType(tdStr):
    arr = re.findall(".*<a\s*href.*>(.*)</a.*", tdStr)
    if len(arr) == 0:
        chinaNameArr = re.match(r'.*<td>(.*)</td>', tdStr)
        return chinaNameArr.group(1)
    else:
        chinaNameArr = re.match(r'.*<a\s*href.*>(.*)</a.*', tdStr)
        return chinaNameArr.group(1)
   

# 根据正则表达式获取字符串 - 获取镇信息
def getTowerInfo(countyInfo, Str):

    result = []
    trArr = re.findall('<tr\s*class=[\"\']towntr[\"\'](?:(?!tr).)*</tr>', Str)
    for trAr in trArr:
        tdArr = re.findall('<td>(?:(?!td).)*</td>', trAr)
        name = getChinaNameFromTdEle2(tdArr[1])
        address = getAddressFromTdEle(tdArr[0])
        code = getCodeFromTdEle(tdArr[0])
        lastCode = countyInfo.get("code")
        dict = {'name': name, 'address': address, 'code': code, 'lastCode':lastCode}
        result.append(dict)
    return result


# 根据正则表达式获取字符串 - 获取村数据
def getVillagetrsInfo(towerInfo, Str):

    result = []
    trArr = re.findall('<tr\s*class=[\"\']villagetr[\"\'](?:(?!tr).)*</tr>', Str)
    for trAr in trArr:
        tdArr = re.findall('<td>(?:(?!td).)*</td>', trAr)
        name = getChinaNameFromTdEle2(tdArr[2])
        address = getAddressFromTdEle(tdArr[0])
        code = getCodeFromTdEle(tdArr[0])
        lastCode = towerInfo.get("code")
        type = getTownAndcountryType(tdArr[1])
        dict = {'name': name, 'address': address, 'code': code, 'lastCode':lastCode, 'town&countryType':type}
        result.append(dict)
    return result






