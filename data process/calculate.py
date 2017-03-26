# -*- encoding: utf-8 -*-
'''
计算预测准确率
'''

import linecache

result = './kdd2011/CFRecomm.txt'
sample = './kdd2011/sampletest.txt'

result_dataline = []
sample_dataline = []
userNum = 0
itemNum = 0
itemCount = 0
alluser = 0
linestart = 1
correct = 0
sum = 0
number = 1000

cyclecount = 0

result_list = {}
sample_list = {}

while cyclecount < number:
    # 获取userId｜ratingNum
    result_data = linecache.getline(result, linestart)
    sample_data = linecache.getline(sample, linestart)
    if result_data == '':
        break
    else:
        alluser += 1
        result_dataspl = result_data.split('|')
        sample_dataspl = sample_data.split('|')
    #print(sample_dataspl)
    # print(dataspl)
    result_userNum = int(result_dataspl[0])
    #print(result_userNum)
    result_itemNum = int(result_dataspl[1])
    sample_userNum = int(sample_dataspl[0])
    #print(sample_userNum)
    sample_itemNum = int(sample_dataspl[1])
    linestart += 1
    # 循环读取一个用户下的ratings
    while itemCount < result_itemNum:
        result_data = linecache.getline(result, linestart)
        #print(result_data)
        result_dataspl = result_data.split('\t')
        #print(result_dataspl)
        sample_data = linecache.getline(sample, linestart)
        sample_dataspl = sample_data.split('\t')
        #print(sample_dataspl)
        # print(dataspl)
        # result_list.setdefault(int(sample_dataspl[0]),int(sample_dataspl[1]))
        result_dataline.append(int(result_dataspl[0]))
        #print(result_dataline)
        sample_list.setdefault(int(sample_dataspl[0]), int(sample_dataspl[1]))
        #print(sample_list)
        # 行计数
        linestart += 1
        itemCount += 1
    #print(result_dataline)
    #print(sample_list)
    if sample_list.get(result_dataline[3]) != -1:
        correct += 1
    if sample_list.get(result_dataline[4]) != -1:
        correct += 1
    if sample_list.get(result_dataline[5]) != -1:
        correct += 1

    result_dataline = []
    sample_dataline = []
    result_list = {}
    sample_list = {}

    itemCount = 0
    cyclecount += 1
    # 用户计数
#print(alluser)
print("The accuracy is : %f" %(correct/(alluser*3)))



