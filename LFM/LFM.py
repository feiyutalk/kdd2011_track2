import random
import re
from collections import Counter
import math
from collections import OrderedDict


user_items = {'1010':[12,1203,123,429]}

#负样本采样，items：全部track   items_pool:抽取最流行的歌曲作为负样本候选
#当前设定item_pool长度100，因此每个user返回的ret长度为min(2*len(items)+1,len(items)+100)
def RandomSelectNegativeSample(items):
    ret = dict()
    for i in items:
        ret[i] = 1
    n = 0
    for i in range(0, len(items) * 3):
        item = items_pool[random.randint(0, len(items_pool) - 1)]
        if item in ret:
            continue
        ret[item] = 0
        n += 1
        if n > len(items):
            break
    return ret


def InitModel(train, F):
    p = dict()
    q = dict()
    for u in train.keys():
        if u not in p:
            p[u] = [random.random()/math.sqrt(F) for x in range(0,F)]

        for item in train[u]:
            if item not in q:
                q[item] = [random.random() / math.sqrt(F) for x in range(0, F)]

    return [p, q]
'''

def InitModel(user_items,F):
    P = dict()
    Q = dict()
    for u in user_items.keys():
        if u not in P:
            P[u] = {}
        for f in range(0,F):
            P[u][f] = 1

    items = user_items.values()
    #这一句可能有问题，items[0]并不一定是所有item里最长的一个，因此可能导致矩阵乘法的问题
    itemLen = len(items[0])
    i = 0
    while i< itemLen:
        ii = items[0][i]
        if ii not in Q:
            Q[ii] = {}
        for f in range(0,F):
            Q[ii][f] = 1
        i += 1
    return [P,Q]
'''

def LatentFactorModel(user_items, F=100, N=100, alpha=0.02, lamb=0.01):
    [P, Q] = InitModel(user_items, F)
    print("Initial model done")
    for step in range(0,N):
        for user, items in user_items.items():
            samples = RandomSelectNegativeSample(items)
            for item, rui in samples.items():
                pui = Predict(user, item, P, Q)
                eui = rui - pui
                for f in range(0, F):
                    P[user][f] += alpha * (eui * Q[item][f] - lamb * P[user][f])
                    Q[item][f] += alpha * (eui * P[user][f] - lamb * Q[item][f])
        alpha *= 0.9
        print("round %d done" % (step+1))
    print("Start pridict samples")
    return [P,Q]


def PersonalRank(G,alpha,root,maxsetup):
    rank = dict()
    #rank = {x:0 for x in G.keys()}
    rank = rank.fromkeys(G.keys(),0)
    rank[root] = 1
    for k in range(maxsetup):
        tmp = dict()
        #tmp = {x:0 for x in G.keys()}
        tmp = tmp.fromkeys(G.keys(),0)
        for i,ri in G.items():
            for j,wij in ri.items():
                if j not in tmp:
                    tmp[j] = 0
                tmp[j] += alpha * rank[i]/(1.0*len(ri))
                if j == root:
                    tmp[j] += 1 - alpha
        rank = tmp


        print('iter:' + str(k) + "\t")
        for key,value in rank.items():
            print("%s:%.3f,\t" % (key,value))
    return rank


#P为dict：user_class,Q为dict，class_item,矩阵相乘，计算user对item(代码中i)的兴趣度
def Recommend(user, item, P, Q):
    rank=0
    for f in range(100):
        puf=P[user][f]
        qfi=Q[item][f]
        rank += puf * qfi
    return rank

def Recommend2(user,item ,P, Q):
    rank = dict()
    for f, puf in P[user].items():
        for i, qfi in Q[f].items():
            if i not in rank:
                rank[i] += puf * qfi
    return rank[item]


def Predict(u, i, p, q):
    return sum(p[u][f] * q[i][f] for f in range(0,len(p[u])))


#用于RandomSelectNegativeSample
def makeItemPool(f1,f2,N):
    pool=[]
    trackCount=[]
    trackList=[]
    with open(f1, 'r') as file1:
        for line in file1:
            if re.match(r'\d+\|\d*', line):
                pass
            else:
                data = line.split('\t')
                trackCount.append(data[0])
    '''
    with open(f2, 'r') as file2:
        for line in file2:
            data=line.split('|')
            trackList.append(data[0])
    '''
    counter = Counter(trackCount)
    topN = counter.most_common(N)
    #print(trackList)
    for item in topN:
        #if item[0] in trackList:
        pool.append(item[0])
    return pool

items_pool=makeItemPool('deletegenre.txt','trackdata2.txt',200)

#读训练集
with open('trainData.txt', 'r') as file:
    user_items={}
    line = file.readline()
    while(re.match(r'(\d+)(\|)(\d*)', line)):
        tracks ={}
        m1 = re.match(r'(\d+)(\|)(\d*)', line)
        num = m1.group(3)
        i = 0
        line= file.readline()
        while(re.match(r'(\d+)(\t)(\d*)', line)):
            m2 = re.match(r'(\d+)(\t)(\d*)', line)
            if int(m2.group(3))>=80:
                tracks[m2.group(1)]=0
            line = file.readline()

        user_items[m1.group(1)]=tracks



#读取测试集
with open('testData.txt', 'r') as file:
   test_user_items=OrderedDict()
   line = file.readline()
   while(re.match(r'(\d+)(\|)(\d*)', line)):
       tracks ={}
       m = re.match(r'(\d+)(\|)(\d*)', line)
       line= file.readline()
       while(re.match(r'(\d+)(\t)(\d*)', line)):
           data = line.split('\t')
           tracks[data[0]]=0
           line = file.readline()

       test_user_items[m.group(1)]=tracks


#def LatentFactorModel(user_items, F=100, N=100, alpha=0.02, lamb=0.01):
#F=特征数量 N=迭代次数
[P, Q] = LatentFactorModel(user_items, 100, 100, 0.03, 0.01)

#预测并输出
with open('testresult.txt', 'w') as f:
    for user in test_user_items:
        f.write("%d|%d" % (int(user), 6))
        f.write("\n")
        if user not in P:
            continue
        for item in test_user_items[user]:
            if item not in Q:
                f.write("%d\t%f" % (int(item), 0.0))
                f.write("\n")
            else:
                f.write("%d\t%f" % (int(item),Recommend(user, item, P, Q)))
                f.write("\n")

#for user in user_items:
#    print(Recommend(str(0), P, Q))

#P/Q的keys都是str类型




