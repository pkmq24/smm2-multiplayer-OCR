import time
import numpy as np
import pyautogui
import cv2
import pytesseract
from PIL import Image
import webbrowser
import os
import math
import _thread
# pip install opencv-python
# sudo apt-get install scrot
# https://www.bilibili.com/video/av81797290?p=2&t=1427
pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract"

#configArea
t1 = time.localtime()
dateS = "{:02d}{:02d}".format(t1.tm_mon,t1.tm_mday)

if not os.path.exists(dateS):
    os.mkdir(os.getcwd()+"\\"+dateS)

fileName = dateS+"/"+dateS+".json"
fileName2 = dateS+"/"+dateS+"-list.json"
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
def erzhihua2(image,threshold):
    ''':type image:Image.Image'''
    image=image.convert('L')
    table=[]
    for i in range(256):
        if i < threshold:
            table.append(1)
        else:
            table.append(0)
    return image.point(table,'1')
def getOCR(props, lang="eng", name="scr", isDebugging = False):
    img = pyautogui.screenshot(region=props) # x,y,w,h
    #img = erzhihua(img,127)
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
    #print([getresult,img])
    return [getresult,img]

def getScore():
    return getOCR([1665,1035,257,80],'eng','scr',1)
def doIt(arr):
    for x in arr:
        if x.find("DY") != -1 or x.find("Xiao") != -1:
            return False
    return True

def getNames(): 
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

def getNames2(): 
    res = []
    img = pyautogui.screenshot(region=[0,0,2560,1440])
    props = [83,1114,377,63]
    res = []
    for i in range(1,4):
        props[0]=props[0]+555
        # 235,449 327,488
        img1 = img.crop((props[0],props[1],props[0]+props[2],props[1]+props[3]))
        img1.save("./d/{}1.png".format(i))
        getresult = pytesseract.image_to_string(img1, lang="jpn").replace("\n","").replace(" ",'')
        if getresult.replace(" ","").replace("\n","") == "":
            getresult = pytesseract.image_to_string(erzhihua(img1,127), lang="jpn").replace("\n","").replace(" ",'')
        getresult2 = "123"
        t0 =time.process_time()
        vSet = list(range(1,11))
        p=0
        while len(getresult2) != 4:
            img2 = erzhihua2(img.crop((215+280+i*550-550,429,i*550-550+330+290+(-10 if i ==1 else 0)+vSet[p],495)),215)
            img2.save("./d/{}2.png".format(i))
            getresult2 = pytesseract.image_to_string(img2, lang="eng", config='--psm 10 digits -c tessedit_char_whitelist=0123456789').replace("\n","").replace(" ",'')
            print(getresult2)
            p+=1
            if p == 10:
                break
            if time.process_time() - t0 >= 2:
                break
        res.append([getresult.replace(" ","").replace("\n",""),getresult2])
    res.append(['','0'])        
    print(res)
    return res
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

def getPoints2(imgg = ''):
    global isThreeRound
    res = []
    if imgg == '': img = pyautogui.screenshot(region=[0,0,2560,1440])
    else: img = imgg
    img.save("after.png")
    deltaX = 0
    P = 0

    if isThreeRound:
        isThreeRound = False
        for i in range(1,4):
            getresult2 = "123"
            t0 = time.process_time()
            p=0
            while len(getresult2) != 4:
                for j in range(-2,3):
                    deltax = j*15
                    img2 = erzhihua2(img.crop((deltax+505+i*540-540,979,deltax+i*540-540+620,1035)),180+p+P)
                    img2.save("./b/{}-3-{}.png".format(i,deltax))
                    getresult2 = pytesseract.image_to_string(img2, lang="eng", config='-c tessedit_char_whitelist=0123456789').replace("\n","").replace(" ",'')
                    print(getresult2,deltaX,deltax,P,p)
                    if len(getresult2)==4: 
                        if deltaX == 0: deltaX = deltax
                        if P == 0: P = p
                        break
                p+=10
                if p == 60:
                    break
                if time.process_time() - t0 >= 4:
                    break
            res.append(getresult2)
        res.append('0')
        f = open("./"+fileName2,"a")
        ss = "{:02d}:{:02d}:{:02d}".format(t.tm_hour,t.tm_min,t.tm_sec)
        f.write("\n{\"time\":\"%s\",\"pointsArr\": ["%(ss)+",".join(res)+"]},")
        f.close()
    else:
        for i in range(1,5):
            getresult2 = "123"
            t0 = time.process_time()
            p=0
            while len(getresult2) != 4:
                for j in range(-2,3):
                    deltax = j*15
                    img2 = erzhihua2(img.crop((deltax+230+i*540-540,979,deltax+i*540-540+345,1035)),180+p+P)
                    img2.save("./b/{}-3-{}.png".format(i,deltax))
                    getresult2 = pytesseract.image_to_string(img2, lang="eng", config='-c tessedit_char_whitelist=0123456789').replace("\n","").replace(" ",'')
                    print(getresult2,deltaX,deltax,P,p)
                    if len(getresult2)==4: 
                        if deltaX == 0: deltaX = deltax
                        if P == 0: P = p
                        break
                p+=10
                if p == 60:
                    break
                if time.process_time() - t0 >= 4:
                    break
            res.append(getresult2)
        f = open("./"+fileName2,"a")
        ss = "{:02d}:{:02d}:{:02d}".format(t.tm_hour,t.tm_min,t.tm_sec)
        f.write("\n{\"time\":\"%s\",\"pointsArr\": ["%(ss)+",".join(res)+"]},")
        f.close()

lastNameT = -3
lastPointT = -2
lastAfterPointT = -3
isThreeRound = False

def getAfter(lastPointT):
    global lastNameT,lastAfterPointT
    while True:
        #比赛结束！记录四个人的名字与分数
        ans4 = getIfReady2()
        print(ans4)
        print(0)
        #print(ans3,ans3.find("确定") != -1,time.process_time(),lastNameT)
        if ans4[0].find("结束") != -1 and time.process_time() - lastAfterPointT >= 3:
            lastAfterPointT = time.process_time()
            _thread.start_new_thread(getPoints2,(ans4[1],))
            break
        if time.process_time() - lastPointT >= 9:
            f = open("./"+fileName2,"a")
            t = time.localtime()
            ss = "{:02d}:{:02d}:{:02d}".format(t.tm_hour,t.tm_min,t.tm_sec)
            f.write("\n{\"time\":\"%s\",\"pointsArr\": ["%(ss)+"]},")
            f.close()
            break

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

while True:
    #比赛开始！记录四个人的名字与分数
    ans3 = ""
    #if lastPointT > lastNameT: ans3 = getIfReady() #当已经记录过分数了 才开始检测是否开新局
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
    #if lastPointT < lastNameT: getresult = getScore() #当开了新局 才开始检测是否记录过分数
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

    #deal.py中把两个json按行数合成一个
    
"""
#比赛开始！记录四个人的名字与分数
    ans3 = ""
    if lastPointT > lastNameT: ans3 = getIfReady() #当已经记录过分数了 才开始检测是否开新局
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
    if lastPointT < lastNameT: getresult = getScore() #当开了新局 才开始检测是否记录过分数
    #getresult = getScore()# 测试用 实际使用时请注释
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
        #{time:"13:16:05", players:["","なめくじ$","ひまたん!","しんけんしょうぶだ!"], pointAfter: 5623}
        t = time.localtime()
        ss = "{:02d}:{:02d}:{:02d}".format(t.tm_hour,t.tm_min,t.tm_sec)
        f.write(" \"pointAfter\": 5{}, \"finishTime\":\"{}\"}}, ".format(ans,ss))
        f.close()
        print("*****PointNow: 5" + ans)
        lastPointT = time.process_time()
        _thread.start_new_thread(getAfter,(lastPointT,))
    time.sleep(0.2)

    #deal.py中把两个json按行数合成一个
"""