# -*- encoding: utf-8 -*-

import random
import linecache

resultcb = './kdd2011/CBRecomm.txt'
resultcf = './kdd2011/CFRecomm.txt'
sample = './kdd2011/sample_1000.txt'

cbid_dataline = []
cbid_copy = []
cbrating_dataline = []
sample_dataline = []
final_list = []
userNum = 0
itemNum = 0
itemCount = 0
alluser = 0
linestart = 1
correct = 0
sum = 0
sum_temp1 = 0
sum_temp2 = 0
number = 1000
#------------------
list = []
list1 = []
#------------------
cyclecount = 0

resultcb_dict = {}
cf_dict = {}
sample_dict = {}
p = 1000
q = 2

for i in [0, 1, 2, 3, 4, 5]:
    list1.append(random.random())
list1.sort()
while cyclecount < number:
    # 获取userId｜ratingNum
    resultcb_data = linecache.getline(resultcb, linestart)
    resultcf_data = linecache.getline(resultcf, linestart)
    sample_data = linecache.getline(sample, linestart)
    if resultcb_data == '':
        break
    else:
        alluser += 1
        resultcb_dataspl = resultcb_data.split('|')
        resultcf_dataspl = resultcf_data.split('|')
        sample_dataspl = sample_data.split('|')
    #print(sample_dataspl)
    # print(dataspl)
    resultcb_userNum = int(resultcb_dataspl[0])
    resultcb_itemNum = int(resultcb_dataspl[1])
    resultcf_userNum = int(resultcf_dataspl[0])
    resultcf_itemNum = int(resultcf_dataspl[1])
    sample_userNum = int(sample_dataspl[0])
    #print(sample_userNum)
    sample_itemNum = int(sample_dataspl[1])
    linestart += 1
    # 循环读取一个用户下的ratings
    while itemCount < resultcb_itemNum:
        resultcb_data = linecache.getline(resultcb, linestart)
        resultcb_dataspl = resultcb_data.split('\t')

        resultcf_data = linecache.getline(resultcf, linestart)
        resultcf_dataspl = resultcf_data.split('\t')

        sample_data = linecache.getline(sample, linestart)
        sample_dataspl = sample_data.split('\t')
        #print(sample_dataspl)
        # print(dataspl)
        # result_list.setdefault(int(sample_dataspl[0]),int(sample_dataspl[1]))
        cbid_dataline.append(int(resultcb_dataspl[0]))
        cbid_copy.append(int(resultcb_dataspl[0]))
        cbrating_dataline.append(int(resultcb_dataspl[1]))
        cf_dict.setdefault(int(resultcf_dataspl[0]), int(resultcf_dataspl[1]))

        sample_dict.setdefault(int(sample_dataspl[0]), int(sample_dataspl[1]))
        # 行计数
        linestart += 1
        itemCount += 1

    #归一化
    for j in [0, 1, 2, 3, 4, 5]:
        sum_temp1 += cbrating_dataline[j]
    if sum_temp1 != 0:
        for j in [0, 1, 2, 3, 4, 5]:
            cbrating_dataline[j] /= sum_temp1

    for j in [0, 1, 2, 3, 4, 5]:
        sum_temp2 += cf_dict.get(cbid_dataline[j])
    if sum_temp2 != 0:
        for j in [0, 1, 2, 3, 4, 5]:
            cf_dict[cbid_dataline[j]] /= sum_temp2

    for j in [0, 1, 2, 3, 4, 5]:
        cbrating_dataline[j] = p*cbrating_dataline[j] + q*cf_dict.get(cbid_dataline[j])
    for j in [0, 1, 2, 3, 4, 5]:
        sum += cbrating_dataline[j]
    cbrating_dataline[1] = (cbrating_dataline[1] + cbrating_dataline[0])/sum
    cbrating_dataline[2] = (cbrating_dataline[2] + cbrating_dataline[1])/sum
    cbrating_dataline[3] = (cbrating_dataline[3] + cbrating_dataline[2])/sum
    cbrating_dataline[4] = (cbrating_dataline[4] + cbrating_dataline[3])/sum
    cbrating_dataline[5] = (cbrating_dataline[5] + cbrating_dataline[4])/sum
    cbrating_dataline[0] = cbrating_dataline[0]/sum


    for i in [0, 1, 2, 3, 4, 5]:
        list.append(random.random())
    list.sort()
    for i in [0, 1, 2, 3, 4, 5]:
        if cbrating_dataline[i] >= list[i]:
            final_list.append(cbid_dataline[i])
            #print(cbid_dataline[i])
            cbid_copy.remove(cbid_dataline[i])
    if len(final_list) >= 3:
        final_list.reverse()
        if sample_dict.get(final_list[0]) != -1:
            correct += 1
        if sample_dict.get(final_list[1]) != -1:
            correct += 1
        if sample_dict.get(final_list[2]) != -1:
            correct += 1
    elif len(final_list) == 2:
        cbid_copy.reverse()
        if sample_dict.get(final_list[0]) != -1:
            correct += 1
        if sample_dict.get(final_list[1]) != -1:
            correct += 1
        if sample_dict.get(cbid_copy[0]) != -1:
            correct += 1
    elif len(final_list) == 1:
        cbid_copy.reverse()
        if sample_dict.get(final_list[0]) != -1:
            correct += 1
        if sample_dict.get(cbid_copy[0]) != -1:
            correct += 1
        if sample_dict.get(cbid_copy[1]) != -1:
            correct += 1
    elif len(final_list) == 0:
        if sample_dict.get(cbid_dataline[3]) != -1:
            correct += 1
        if sample_dict.get(cbid_dataline[4]) != -1:
            correct += 1
        if sample_dict.get(cbid_dataline[5]) != -1:
            correct += 1

    list = []
    sum = 0
    sum_temp1 = 0
    sum_temp2 = 0

    cf_dict = {}
    sample_dict = {}
    cbid_dataline = []
    cbid_copy = []
    cbrating_dataline = []
    final_list = []

    resultcb_dataline = []
    resultcb_list = {}
    sample_list = {}

    itemCount = 0
    cyclecount += 1
    # 用户计数
#print(alluser)
print("The accuracy is : %f" %(correct/(alluser*3)))