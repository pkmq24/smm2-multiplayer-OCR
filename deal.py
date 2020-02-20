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
