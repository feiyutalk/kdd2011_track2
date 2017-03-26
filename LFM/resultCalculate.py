from collections import OrderedDict
import re

def resultCal():
    with open('testresult.txt', 'r') as file:
        predict = []
        line = file.readline()
        while (re.match(r'(\d+)(\|)(\d*)', line)):
            tracks = {}
            #m = re.match(r'(\d+)(\|)(\d*)', line)
            line = file.readline()
            while (re.match(r'(\d+)(\t)(\d*)', line)):
                line = line.strip('\n')
                data = line.split('\t')
                tracks[data[0]] = float(data[1])
                line = file.readline()

            predict.append(tracks)

    with open('testData.txt', 'r') as file:
        result = []
        line = file.readline()
        while (re.match(r'(\d+)(\|)(\d*)', line)):
            tracks = {}
            #m = re.match(r'(\d+)(\|)(\d*)', line)
            line = file.readline()
            while (re.match(r'(\d+)(\t)(\d*)', line)):
                line = line.strip('\n')
                data = line.split('\t')
                tracks[data[0]] = float(data[1])
                line = file.readline()

            result.append(tracks)

    rightSum=0
    wrongSum=0
    for i in range(len(predict)):
        predict_sort=sorted(predict[i].items(),key=lambda item:item[1], reverse = True)
        result_sort = sorted(result[i].items(),key=lambda item:item[1],reverse = True)
        predict_sort_keys=[]
        result_sort_keys=[]
        for i in predict_sort:
            predict_sort_keys.append(i[0])
        for i in result_sort:
            result_sort_keys.append(i[0])
        print(predict_sort_keys)
        print(result_sort_keys)
        if predict_sort_keys[0]==result_sort_keys[0] or predict_sort_keys[0]==result_sort_keys[1] or predict_sort_keys[0]==result_sort_keys[2]:
            rightSum += 1
        else: wrongSum+=1
        if predict_sort_keys[1]==result_sort_keys[0] or predict_sort_keys[1]==result_sort_keys[1] or predict_sort_keys[1]==result_sort_keys[2]:
            rightSum += 1
        else: wrongSum+=1
        if predict_sort_keys[2]==result_sort_keys[0] or predict_sort_keys[2]==result_sort_keys[1] or predict_sort_keys[2]==result_sort_keys[2]:
            rightSum += 1
        else: wrongSum+=1

    print("Acrracy:%.4f" % (rightSum/(rightSum+wrongSum)))

resultCal()