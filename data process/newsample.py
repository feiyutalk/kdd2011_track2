# -*- encoding: utf-8 -*-

import csv
import linecache

deletegenre = open('./kdd2011/deletegenre.txt', 'w')
f = "./kdd2011/trainIdx2.txt"           # 返回一个文件对象
#writer = csv.writer(csvfile)

dataline = [0, 0, 0, 0]
userNum = 0
itemNum = 0
itemchange = 0
itemCount = 0
linestart = 1
#lineend = 0
cyclecount = 0
bigcycle = 0
list = []
filepath = "./kdd2011/genreData2.txt"
dict = {}
start = 1
genreNum = 0
while genreNum < 567:
    genredata = linecache.getline(filepath, start)
    dict.setdefault(int(genredata))
    start += 1
    genreNum += 1
linecache.clearcache()
#249012个用户
while userNum<13000:
    while cyclecount<500:
        #获取userId｜ratingNum
        data = linecache.getline(f, linestart)
        dataspl = data.split('|')
        #print(dataspl)
        userNum = int(dataspl[0])
        itemNum = int(dataspl[1])
        linestart += 1
        # 循环读取一个用户下的ratings
        while itemCount < itemNum:
            data = linecache.getline(f, linestart)
            dataspl = data.split('\t')
            # print(dataspl)
            dataline[1] = int(dataspl[0])
            dataline[2] = int(dataspl[1])
            # 写csv
            datastr = str(dataline[1]) + "\t" + str(dataline[2]) + "\n"
            if dataline[1] in dict:
                datastr = ' '
            else:
                list.append(datastr)
                itemchange += 1
            # 行计数
            linestart += 1
            itemCount += 1
        itemNum = itemchange
        datastr = str(userNum) + "|" + str(itemNum) + "\n"
        list.insert(0, datastr)
        #writer.writerow(['%s'%datastr])
        deletegenre.writelines(list)

        list = []
        itemchange = 0
        itemCount = 0
        cyclecount += 1
        #用户计数
        userNum += 1
    #cyclecount计数清零，释放内存
    linecache.clearcache()
    cyclecount = 0
    bigcycle += 1
    print(bigcycle)

deletegenre.close()


