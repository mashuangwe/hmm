from .._compat import *
import re

MIN_FLOAT = -3.14e100

PrevStates = {
    'B': 'SE',
    'M': 'MB',
    'E': 'MB',
    'S': 'SE'
}

'''
start_p pi
trans_p a
emit_p  b
'''

# viterbi decode
def viterbi(obs, states, start_p, trans_p, emit_p):
    V = [{}]    # 前向概率，数组下标为时间，元素为到达该时刻各状态的最大概率，包括观测概率
    path = {}   # 到达某一点的最佳路径记录, key:当前点，value:到达该点的最佳路径，空间换时间，后面无需回头

    # init
    for y in states:
        V[0][y] = start_p[y] + emit_p[y].get(obs[0], MIN_FLOAT)
        path[y] = [y]
    # forward
    for t in range(1, len(obs)):
        newPath = {}
        for y in states:    # 当前状态
            emp = emit_p[y].get(obs[t], MIN_FLOAT)
            (prob, state) = max([(V[t - 1][y0] + trans_p[y0].get(y, MIN_FLOAT) + emp, y0) for y0 in PrevStates])  # y0为前一状态
            V[t][y] = prob
            newPath[y] = path[state] + [y]
        path = newPath

    (prob, state) = max((V[len(obs) - 1][y], y) for y in 'ES')    # 确定最后一个状态，来确定最佳路径

    return prob, path[state]

def __cut(sentence):
    global start_P, trans_P, emit_P
    prob, pos_list = viterbi(sentence, 'BMES', start_P, trans_P, emit_P)
    index = 0

    for i, char in enumerate(sentence):
        pos = pos_list[i]
        if pos == 'B':
            index = i
        elif pos == 'E':
            yield sentence[index : i + 1]
            index = i + 1
        elif pos == 'S':
            yield char
            index = i + 1

    if index < len(sentence):
        yield sentence[index : ]

re_han = re.compile('([\u4E00-\u9FD5]+)')
re_skip = re.compile('([a-zA-Z0-9]+(?:\.\d+)?%?)')

Force_Split_Words = set([])

def cut(sentence):
    sentence = strdecode(sentence)
    blocks = re_han.split(sentence)
    for blk in blocks:
        if re_han.match(blk):
            for word in __cut(blk):
                if word not in Force_Split_Words:
                    yield word
                else:
                    for c in word:
                        yield c
        else:
            for x in re_skip(blk):
                if x:
                    yield x

def strdecode(sentence):
    if not isinstance(sentence, str):
        try:
            sentence = sentence.decode('utf-8')
        except:
            sentence = sentence.decode('gbk', 'ignore')
    return sentence

