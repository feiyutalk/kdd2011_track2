# -*- encoding: utf-8 -*-

import csv
import linecache

file = './kdd2011/testIdx2.txt'
filesample = open('./kdd2011/sample_1000.txt', 'w')

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
dict = {}

while userNum < 1001:
    while cyclecount<100:
        #获取userId｜ratingNum
        data = linecache.getline(file, linestart)
        dataspl = data.split('|')
        #print(dataspl)
        userNum = int(dataspl[0])
        itemNum = int(dataspl[1])
        linestart += 1
        # 循环读取一个用户下的ratings
        if itemNum != 0:
            while itemCount < itemNum:
                data = linecache.getline(file, linestart)
                dataspl = data.split('\t')
                # print(dataspl)
                dataline[1] = int(dataspl[0])
                dataline[2] = int(dataspl[1])
                # 写csv
                datastr = str(dataline[1]) + "\t" + str(dataline[2]) + "\n"
                list.append(datastr)
                # 行计数
                linestart += 1
                itemCount += 1

            datastr = str(userNum) + "|" + str(itemNum) + "\n"
            list.insert(0, datastr)
            # writer.writerow(['%s'%datastr])
            filesample.writelines(list)

        else:
            datastr = str(userNum) + "|" + str(itemNum) + "\n"
            list.insert(0, datastr)
            # writer.writerow(['%s'%datastr])
            filesample.writelines(list)

        list = []
        itemchange = 0
        itemCount = 0
        cyclecount += 1

    #cyclecount计数清零，释放内存
    linecache.clearcache()
    cyclecount = 0
    bigcycle += 1
    print(bigcycle)

filesample.close()
