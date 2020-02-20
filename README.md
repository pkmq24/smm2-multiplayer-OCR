
个人博客：https://puluter.cn
本文也可在：https://puluter.cn/20200220/smm2-multiplayer-statisics/  查看

# 起源
看桀哥直播，突然迸发了一个想法，多人对战可不可以用OCR来记录数据呢？于是就开坑开始写下了代码。本文为自己记录一下开发过程，解释代码内容，记录开发心得。

# 程序内容
## 文件
整个程序分为两个文件<code>mario.py</code>和<code>deal.py</code>，前者的作用是进行OCR识别并将数据记录到json文件中。后者的作用是处理json文件中的数据，产生数据分析。

# mario.py
## ocr流程

1. [比赛开始] 记录四个人的分数与名字
2. [比赛结束] 记录桀哥分数

### 为什么不记录比赛结束后的分数呢？
因为经测试，比赛结束后的分数出现时间极短，而且因为smm2中颜色是渐变的，有的时候还没有到达我的识别颜色，桀哥就会直接按跳过，就出现了无法记录的问题。
## 具体函数

### erzhihua - 二值化函数
```python
def erzhihua(image,threshold):
    ''':type image:Image.Image'''
    image=image.convert('L')
    table=[]
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    return image.point(table,'1') 
```
基础的二值化函数，为提高OCR识别准确率而使用
### getOCR - OCR的基础函数
```python
def getOCR(props, lang="eng", name="scr", isDebugging = False):
    img = pyautogui.screenshot(region=props) # x,y,w,h
    if isDebugging:
        img.save(name+".png")
    getresult = pytesseract.image_to_string(img, lang=lang).replace("\n","").replace(" ",'')
    return getresult


def getOCR2(props, lang="eng", name="scr", isDebugging = False):
    img = pyautogui.screenshot(region=[0,0,2560,1440])
    img1 = img.crop((props[0],props[1],props[0]+props[2],props[1]+props[3])) # x,y,w,h
    if isDebugging:
        img.save(name+".png")
    getresult = pytesseract.image_to_string(img1, lang=lang).replace("\n","").replace(" ",'')
    return [getresult,img]
```
(props,lang,name,isDebugging)

- props：要截取的画面区域
- lang：要进行OCR识别的语言
- name：如果在debug状态，会以此名称存下img图片
- isDebugging：是否在debug状态

这个函数的主要作用是截取显示屏的某一个区域，并返回OCR结果。

但是它存在一个问题。当比赛开始的时候，OCR需要识别图上共八个区域的信息（四个名字+四个分数）
用这个函数会导致要截图八次，这个过程是比较耗时的，所以改进了getOCR2()

#### getOCR2
- props：要截取的画面区域
- lang：要进行OCR识别的语言
- name：如果在debug状态，会以此名称存下img图片
- isDebugging：是否在debug状态

getOCR2的主要进步是，它只会截图一次，返回给调用函数全屏幕的信息，再进行裁剪图片操作，这样可以减少延时。

#### 小细节
```python
getresult = pytesseract.image_to_string(img1, lang=lang).replace("\n","").replace(" ",'')
```
这里特意有一个<code>.replace("\n","").replace(" ",'')</code>是因为OCR识别过程中经常会出现多余的空格和回车，用这个来去掉这些多余的字符。
### getIfReady - 确定是否比赛即将开始/结束
```python
def getIfReady():#比赛开始
    ress = getOCR2([1069,250,528,121],"chi_sim","chn",True)
    return ress

def getIfReady2():#比赛最后
    ress = getOCR2([736,1240,405,90],"chi_sim","chn2",True)
    img = ress[1]
    while abs(img.getpixel((1402,536))[2] - 254) >= 5 and abs(img.getpixel((869,543))[2] - 254) >= 5:
        img = pyautogui.screenshot(region=[0,0,2560,1440])
        time.sleep(0.05)
    ress[1] = img
    return ress
```
#### 比赛开始
本质上是对某个区域进行OCR识别，来获取对应信息。
![比赛开始的OCR识别内容](http://q5vnkmxjg.bkt.clouddn.com/chn.png)
在比赛开始的时候，屏幕上会有一句“已确定对战的成员”。用OCR对这个区域进行识别，并对结果中有没有“确定”两个字进行确认，就可以知道是否比赛开始了。至于为什么不对整句话识别，因为OCR会有识别误差，不能保证所有字都识别正确。

#### 比赛结束
直接对某个坐标取色，当色合理后即为比赛结束。
![比赛结束后整体UI](http://q5vnkmxjg.bkt.clouddn.com/3人.png)
![上述函数中截图的部分](http://q5vnkmxjg.bkt.clouddn.com/chn2.png)
在比赛结束后，“结束”这部分的颜色必然是白色的，而在其他时候一般不会。所以取几个点色，如果都是白色，那么就可以知道比赛结束了。
### getNames - OCR识别ID和分数
```python
res = []
    img = pyautogui.screenshot(region=[0,0,2560,1440])
    props = [-259,1114,377,63]
    res = []
    for i in range(1,5):
        props[0]=props[0]+555
        # 235,449 327,488

        img1 = img.crop((props[0],props[1],props[0]+props[2],props[1]+props[3]))
        img1.save("./b/{}1.png".format(i))
        getresult = pytesseract.image_to_string(img1, lang="jpn").replace("\n","").replace(" ",'')
        if getresult.replace(" ","").replace("\n","") == "":
            getresult = pytesseract.image_to_string(erzhihua(img1,127), lang="jpn").replace("\n","").replace(" ",'')
        
        getresult2 = "123"
        t0 =time.process_time()
        vSet = list(range(1,11))
        p=0
        while len(getresult2) != 4:
            img2 = erzhihua2(img.crop((215+i*555-555,429,i*555-555+330+(-10 if i ==1 else 0)+vSet[p],495)),215)
            img2.save("./b/{}2.png".format(i))
            getresult2 = pytesseract.image_to_string(img2, lang="eng", config='--psm 10 digits -c tessedit_char_whitelist=0123456789').replace("\n","").replace(" ",'')
            #print(getresult2)
            p+=1
            if p == 10:
                break
            if time.process_time() - t0 >= 2:
                break
        if getresult2 == "":
            res.append([getresult,-1])
        else:
            res.append([getresult.replace(" ","").replace("\n",""),int(getresult2)])
    res.sort(key = lambda x: 0 if x[1] == -1 else -1)
    fl = True#是否是三人
    for x in res:
        if x[1]!=-1:
            fl = False
    if fl:
        return []
        
    print(res)
    return res
```
其实就是对固定的坐标进行截图并OCR处理。
![4人参与的时候的截图](http://q5vnkmxjg.bkt.clouddn.com/root.png)
![11](http://q5vnkmxjg.bkt.clouddn.com/11.png)
![12](http://q5vnkmxjg.bkt.clouddn.com/12.png)
![13](http://q5vnkmxjg.bkt.clouddn.com/13.png)
![14](http://q5vnkmxjg.bkt.clouddn.com/14.png)
这里有个小点，需要对图片进行二值化后再进行OCR才能保证识别准确率。
<code>getNames2()</code>是对两人进行处理，主要就是换坐标，这里就不赘述

### getBefore - 数据处理并存储函数

```python
def getBefore(ans3,typea):
    global lastNameT
    if typea == 1:#3人
        ans1 = getNames2()
        if ans1 != []:
            ans2 = ["[\"{}\",{}]".format(ans1[x][0],ans1[x][1]).replace("_","").replace("DYXiaoJie","DY_XiaoJie") for x in range(4)]
            f = open("./"+fileName,"a",encoding="UTF-8")
            t = time.localtime()
            timeStr = "\n\t{{\"time\":\"{:02d}:{:02d}:{:02d}\", \"players\":[".format(t.tm_hour,t.tm_min,t.tm_sec)
            f.write(timeStr+",".join(ans2)+"],")
            f.close()
        else:
            f = open("./"+fileName,"a",encoding="UTF-8")
            t = time.localtime()
            timeStr = "\n\t{{\"time\":\"{:02d}:{:02d}:{:02d}\", \"players\":[],".format(t.tm_hour,t.tm_min,t.tm_sec)
            f.write(timeStr)
            f.close()
    elif typea == 2:#4人
        ans1 = getNames()
        if ans1 != []:
            ans2 = ["[\"{}\",{}]".format(ans1[x][0],ans1[x][1]).replace("_","").replace("DYXiaoJie","DY_XiaoJie") for x in range(4)]
            f = open("./"+fileName,"a",encoding="UTF-8")
            t = time.localtime()
            timeStr = "\n\t{{\"time\":\"{:02d}:{:02d}:{:02d}\", \"players\":[".format(t.tm_hour,t.tm_min,t.tm_sec)
            f.write(timeStr+",".join(ans2)+"],")
            f.close()
        else:
            f = open("./"+fileName,"a",encoding="UTF-8")
            t = time.localtime()
            timeStr = "\n\t{{\"time\":\"{:02d}:{:02d}:{:02d}\", \"players\":[],".format(t.tm_hour,t.tm_min,t.tm_sec)
            f.write(timeStr)
            f.close()
```
### getScore - 判断是否比赛结束并OCR识别分数
```python
def getScore():
    return getOCR([1665,1035,257,80],'eng','scr',1)
```
![比赛结束的截图](http://q5vnkmxjg.bkt.clouddn.com/赢.png)
![实际截图的区域](http://q5vnkmxjg.bkt.clouddn.com/p.png)
## 运行流程 - 主函数


```python
while True:
    #比赛开始！记录四个人的名字与分数
    ans3 = ""
    ans3 = getIfReady()
    if ans3 != "":
        if ans3[0].find("确定") != -1 and time.process_time() - lastNameT >= 3:
            lastNameT = time.process_time()
            #908,1225 [0] == 255→三个人
            if abs(ans3[1].getpixel((908,1225))[0] - 255) <=2 and abs(ans3[1].getpixel((902,1187))[0] - 255) <=2:#三人！
                print(1)
                isThreeRound = True
                _thread.start_new_thread(getBefore,(ans3,1))
                continue
            _thread.start_new_thread(getBefore,(ans3,2))

    #进入比赛结束的分数界面
    getresult = ""
    getresult = getScore()# 测试用 实际使用时请注释
    pos = getresult.find("1000")
    if pos != -1:#ScoreBoardPage
        if time.process_time() - lastPointT <= 3:
            time.sleep(1)
            continue
        print(getresult)
        tmp = getresult
        ans = ""
        ansOlder = ""
        ansOlderer = ""
        while True:
            getresult = getScore()
            pos = getresult.find("1000")
            point = ""
            if pos != -1:
                point = getresult[pos-4:pos-1]
                ansOlderer = ansOlder
                ansOlder = ans
                ans = point
            else:
                ans = ansOlder if ansOlder!="" else ansOlderer
                break
            if ansOlderer == point:
                break
            time.sleep(0.1)
        print(ans,ansOlder,ansOlderer)
        if ans == "" and ansOlder == "" and ansOlderer == "":
            ans = tmp[0:3]
        f = open("./"+fileName,"a",encoding="UTF-8")
        t = time.localtime()
        ss = "{:02d}:{:02d}:{:02d}".format(t.tm_hour,t.tm_min,t.tm_sec)
        f.write(" \"pointAfter\": 5{}, \"finishTime\":\"{}\"}}, ".format(ans,ss))
        f.close()
        print("*****PointNow: 5" + ans)
        lastPointT = time.process_time()
        _thread.start_new_thread(getAfter,(lastPointT,))
    time.sleep(0.2)
```

我们来一点一点看。

### 比赛开始 - 分数记录
```python
    #比赛开始！记录四个人的名字与分数
    ans3 = ""
    ans3 = getIfReady()
    if ans3 != "":
        if ans3[0].find("确定") != -1 and time.process_time() - lastNameT >= 3:
            lastNameT = time.process_time()
            #908,1225 [0] == 255→三个人
            if abs(ans3[1].getpixel((908,1225))[0] - 255) <=2 and abs(ans3[1].getpixel((902,1187))[0] - 255) <=2:#三人！
                print(1)
                isThreeRound = True
                _thread.start_new_thread(getBefore,(ans3,1))
                continue
            _thread.start_new_thread(getBefore,(ans3,2))
```
> PS：这里需要反思一下自己的乱定变量名的问题，请大家不要学我，设一些ans3 ans2 ans1这样的变量名。

首先调用前述<code>getIfReady()</code>函数，看里面是否有<code>确定</code>存在，并通过两次识别时间间距<code>time.process_time() - lastNameT >= 3</code>防止短时间内大量重复建立线程。

再进行识别取色判断这盘游戏有几名玩家参与。
![4人参与的时候的截图](http://q5vnkmxjg.bkt.clouddn.com/root.png)

取色是取 已知如果四人时不是黄色的点。如果发现是黄色（背景色）就可以知道是三人局。

接下来调用前述<code>getBefore()</code>函数，利用python中<code>_thread</code>模块，建立一个线程，防止运行阻塞主线程。

> 注意！不建议使用_thread模块，建议换用更新的，我用它单纯是因为我懒（

### 比赛结束
```python
#进入比赛结束的分数界面
    getresult = ""
    getresult = getScore()
    pos = getresult.find("1000")
    if pos != -1:#ScoreBoardPage
        if time.process_time() - lastPointT <= 3:
            time.sleep(1)
            continue
        print(getresult)
        tmp = getresult
        ans = ""
        ansOlder = ""
        ansOlderer = ""
        while True:
            getresult = getScore()
            pos = getresult.find("1000")
            point = ""
            if pos != -1:
                point = getresult[pos-4:pos-1]
                ansOlderer = ansOlder
                ansOlder = ans
                ans = point
            else:
                ans = ansOlder if ansOlder!="" else ansOlderer
                break
            if ansOlderer == point:
                break
            time.sleep(0.1)
        print(ans,ansOlder,ansOlderer)
        if ans == "" and ansOlder == "" and ansOlderer == "":
            ans = tmp[0:3]
        f = open("./"+fileName,"a",encoding="UTF-8")
        t = time.localtime()
        ss = "{:02d}:{:02d}:{:02d}".format(t.tm_hour,t.tm_min,t.tm_sec)
        f.write(" \"pointAfter\": 5{}, \"finishTime\":\"{}\"}}, ".format(ans,ss))
        f.close()
        print("*****PointNow: 5" + ans)
        lastPointT = time.process_time()
        _thread.start_new_thread(getAfter,(lastPointT,))
    time.sleep(0.2)
```

先从<code>getScore()</code>的返回值中搜索**1000**,因为无论什么情况下，只要是结束，就一定会有这个1000存在。（或许红名就没了？我也不知道，桀哥没红名过）
如果搜索到了，再来检测上次开线程的时间，防止短时间内开大量线程。
因为smm2里，人物分数是会有个动画，逐渐变大的，所以加入了14~29行的多次OCR取最终值。
最后用文件操作存入比赛后分数。

# deal.py
不多解释了，就是个数据分析的py文件，源码丢在这了
```python
import json
import time
import math

# 配置部分
t1 = time.localtime()
dateS = "/{:02d}{:02d}".format(t1.tm_mon,t1.tm_mday)
filename = dateS+dateS+".json"
startPoint = 5657

# 处理部分
f = open("./"+filename,"r",encoding="utf-8")
str0 = f.read()
f.close()

jsonObj = json.loads(str0)
users = {}
times = []
points = []
chaArr = [[0,0],[0,0],[0,0],[0,0]]
rawPointsList = []

avgPoints = [[],[],[]]# all, wins, loses

def doIt(timeA):
    sec = int(round(timeA) % 60)
    minn = int(round(timeA) // 60)
    return "{:3d}:{:02d}".format(sec,minn)

lastPoint = startPoint
for x in jsonObj["data"]:
    timeObj = [time.strptime("2020 01 04 "+x["time"],"%Y %m %d %H:%M:%S"),time.strptime("2020 01 04 "+x["finishTime"],"%Y %m %d %H:%M:%S"),time.strptime("2020 01 04 "+jsonObj["data"][0]["time"],"%Y %m %d %H:%M:%S")]
    if x.get("desc",0)!=0:
        print("【{}】{}".format(doIt(time.mktime(timeObj[0])-time.mktime(timeObj[2])),x["desc"]))
    times.append([x["time"],time.mktime(timeObj[1])-time.mktime(timeObj[0])])
    points.append([x["time"],int(x["pointAfter"])-lastPoint])
    rawPointsList.append(int(x["pointAfter"]))

    pointsSum = 0
    idx = -1 if len(x["players"]) == 0 else sum([i for i in range(4) if x["players"][i][0]=="DY_XiaoJie"])
    for y in x["players"]:
        if y[0] == "DY_XiaoJie": continue
        users[y[0]] = users.get(y[0],{"win":0,"lose":0})# uesr的win/lose
        if int(x["pointAfter"])-lastPoint > 0:
            users[y[0]]["lose"] += 1
        else: users[y[0]]["win"] += 1
        pointsSum += y[1]
    
    if pointsSum == 0:
        lastPoint = int(x["pointAfter"])
        continue
    avgPoints[0].append(pointsSum)
    if int(x["pointAfter"])-lastPoint > 0:
        if len(x["players"]) != 0: chaArr[idx][0] += 1
        avgPoints[1].append(pointsSum)
    else:
        if len(x["players"]) != 0: chaArr[idx][1] += 1
        avgPoints[2].append(pointsSum)
    lastPoint = int(x["pointAfter"])

# general
timesMax = max(times, key=lambda x:x[1])
timesMin = min(times, key=lambda x:x[1])

pointMax = max(points, key=lambda x:x[1])
pointMin = min(points, key=lambda x:x[1])

pointsList = [points[x][1] for x in range(len(points))]

winTime = sum([1 for x in pointsList if x > 0])
loseTime = sum([1 for x in pointsList if x < 0])
drawTime = sum([1 for x in pointsList if x == 0])

winPlusPoint = sum([x for x in pointsList if x>0])/winTime
loseMinusPoint = sum([x for x in pointsList if x<0])/loseTime

winRate = winTime / (winTime+loseTime+drawTime)
soupTime = sum([1 for x in pointsList if x > -3 and x < 0])

# users
biggestPresentPointer = max(users.items(),key = lambda x: x[1]["lose"])
biggestStealPointer = max(users.items(),key = lambda x: x[1]["win"])
biggestCompetitor = max(users.items(),key = lambda x: x[1]["win"]+x[1]["lose"])

# scores
#print(avgPoints)
avgPoint = [round(100 * sum(x)/len(x)/3)/100 for x in avgPoints]

print("times(max,min):",timesMax, timesMin,"","points(max,min):", pointMax, pointMin,"","pointsList,winCnt,loseCnt,drawCnt,winRate,soupCnt:", pointsList, winTime, loseTime, drawTime, winRate, soupTime, "","给桀哥送分最多/最少的人，遇到桀哥最多次的人：",biggestPresentPointer,biggestStealPointer,biggestCompetitor,"","胜平负的平均分段, 各角色胜率：",avgPoint,chaArr, sep="\n")

with open("./data/"+filename[0:4]+"-points.csv","w",encoding="utf-8") as f:
    f.write("\n".join([str(x["pointAfter"]) for x in jsonObj["data"]]))

arr1 = list(jsonObj["data"])
endPoint = arr1[-1]["pointAfter"]
date = filename[1:5]
anss = """
【{}|胜{}|负{}|汤{}|{}→{}】

【{}】被桀哥吃分{}次，荣获今日最惨
【{}】遇到桀哥{}次，桀哥输掉{}次，荣获今日最佳
【{}】今日与桀哥遇到{}次
桀哥胜利时，他人的平均分段为【{}】
桀哥失败时，他人的平均分段为【{}】

今日，最长游戏时间为【{}s】，出现在下午【{}】的对局中
今日，最短游戏时间仅【{}s】，出现在下午【{}】的对局中
"""

print(anss.format(date,winTime,loseTime,soupTime,startPoint,endPoint,biggestPresentPointer[0],biggestPresentPointer[1]["lose"],biggestStealPointer[0],biggestStealPointer[1]["win"]+biggestStealPointer[1]["lose"],biggestStealPointer[1]["win"],biggestCompetitor[0],biggestCompetitor[1]["win"]+biggestCompetitor[1]["lose"],avgPoint[1],avgPoint[2],timesMax[1],timesMax[0],timesMin[1],timesMin[0]))
names = ["马里奥","路易","小蓝","小红"]
for x in range(4):
    rate = round(chaArr[x][0]/(chaArr[x][0]+chaArr[x][1])*100)/100
    print(names[x]+" 出场了{}次，胜率为：{}".format(chaArr[x][0]+chaArr[x][1],rate))
print("""
（技术：OCR识别）
@Victoricaaaaa""")

maxx = max(rawPointsList)
minn = min(rawPointsList)

step = 5
arr2 = [(x-minn)//step for x in rawPointsList]
row = (maxx-minn+1) // step + 1
strs = ["".center(len(arr2)+2) for x in range(row)]
p = 0
for x in arr2:
    strs[row - x -1] = strs[row - x -1][0:p]+"*"+strs[row - x -1][p+1:]
    for j in range(row - x, row):
        strs[j] = strs[j][0:p]+"*"+strs[j][p+1:]
    p+=1
for x in strs:
    print(x)
    

f = open("./"+dateS+dateS+"-list.json","r",encoding="utf-8")
str0 = f.read()
f.close()

jsonObj1 = json.loads(str0)
print(jsonObj1)
pointsLast = startPoint
eatP = 0
pt = 0

eatCnt = 0
lossCnt = 0

for i in range(len(jsonObj["data"])):
    posJ = sum([x if jsonObj["data"][i]["players"][x][0] == "DY_XiaoJie" else 0 for x in range(4) ])
    # print(posJ,i,pt)
    if i == len(jsonObj["data"]) or pt == len(jsonObj1["data"]):
        break
    while jsonObj1["data"][pt]["pointsArr"][posJ] != jsonObj["data"][i]["pointAfter"]:
        i += 1
        if i == len(jsonObj["data"]) or pt == len(jsonObj1["data"]):
            break
        posJ = sum([x if jsonObj["data"][i]["players"][x][0] == "DY_XiaoJie" else 0 for x in range(4)])
        # print(jsonObj1["data"][pt],jsonObj["data"][i])
    
    if i != 0: isWinned = jsonObj["data"][i]["pointAfter"] - jsonObj["data"][i-1]["pointAfter"] > 0
    else: isWinned = jsonObj["data"][i]["pointAfter"] - startPoint > 0
    for j in range(4):
        if jsonObj["data"][i]["players"][j][1] == 4501: 
            lossCnt += 1
            continue
        eatP += jsonObj["data"][i]["players"][j][1] - jsonObj1["data"][pt]["pointsArr"][j]
        print(jsonObj["data"][i]["players"][j],pt,i,j,jsonObj1["data"][pt]["pointsArr"][j],jsonObj["data"][i]["players"][j][1] - jsonObj1["data"][pt]["pointsArr"][j])
        eatCnt += 1
    pt += 1

print (eatP)
```

# 后记
OCR的识别精度其实并不是很高，所以每天晚上要自己手动校准一遍名字，还是有点累的。而且目前的版本并不是很精美，需要2k分辨率支持，也不能把窗口放在后台，如果后面有时间再改吧。
求个star~