'''
根据词典分词
求一个句子的最大概率的分词方式
动态规划，递推
'''

# 词典，hash, 词 -> 出现概率
FREQ = {}

# 根据词典建立 DAG      directed acyclic graph
def get_DAG(sentence):
    DAG = {}
    N = len(sentence)
    for k in range(N):
        templist = []
        frag = sentence[k]
        i = k
        while i < N and frag in FREQ:
            if frag in FREQ:
                templist.append(frag)
            i += 1
            frag = sentence[k : i + 1]

        if not templist:
            templist.append(k)
        DAG[k] = templist
    return DAG

from math import *
total = 100

def calc(sentence, DAG, route):
    N = len(sentence)
    route[N] = (0, 0)
    logtotal = log(total)
    for idx in range(N - 1, -1, -1):
        route[idx] = max((log(FREQ.get(sentence[idx : x + 1]) or 1) - \
                          logtotal + route[x + 1][0], x) for x in DAG[idx])



