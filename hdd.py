#!/usr/bin/python
# coding=UTF-8
def read_dict(fo):
    s = fo.readline()
    s = s.split()
    dict = {}
    for i in range(0, len(s), 2):
        if (s[i + 1][0] == '['):
            dict[s[i]] = eval(s[i + 1])
        else:
            if (s[i + 1][0] == '0'):
                dict[s[i]] = int(s[i + 1][2:], 2)
            else:
                dict[s[i]] = s[i + 1]
    return dict


def init():
    global Grammar
    global GrammarObj
    fo = open('d:\py\ProbabilityGrammar\\input.txt', 'r')
    ##get structure imformation
    # get Roof
    Roof = read_dict(fo)

    # get Wall
    Wallnum = read_dict(fo)
    Wall = [0, 0, 0, 0]
    for i in range(int(Wallnum['Num'])):
        Wall[i] = read_dict(fo)

    # get Door
    Door = read_dict(fo)

    # get Window
    Windownum = read_dict(fo)
    Window = [0, 0, 0, 0]
    for i in range(int(Windownum['Num'])):
        Window[i] = read_dict(fo)

    # get GrammarObj
    Grammarobj = read_dict(fo)
    for i in range(int(Grammarobj['GrammarObject'])):
        GrammarObj = dict(GrammarObj, **read_dict(fo))

    # get Grammar
    Grammarnum = read_dict(fo)
    for i in range(int(Grammarnum['GrammarNum'])):
        temp = fo.readline()
        Grammar.append(temp.split())
        Grammar[i][3] = float(Grammar[i][3])
    fo.close()


def progra(root):
    father = GrammarObj[root]
    if father in [1, 2, 4, 8]:
        return (1.0)
    res = 0
    for g in Grammar:
        if g[0] == root:
            temp = g[-1]
            for i in range(1,len(g)-1):
                Name = g[i]
                Proba = progra(Name)
                temp *= Proba
            if (temp > res):
                res, bes = temp, g
    # print '%s(%d) = %s(%d) + %s(%d)\n P = %f'%(root,father,left,lchild,right,rchild,res)
    BestRule[root] = bes
    return res


def outp(root):
    father = GrammarObj[root]
    if father in [1, 2, 4, 8]:
        return
    g = BestRule[root]
    left, right = g[1], g[2]
    fw.write('%s -> %s || %s\n' % (root, left, right))
    outp(left)
    outp(right)


import fileinput
import re

GrammarObj = {}
Grammar = []
BestRule = {}
init()
res = progra('Building')
fw = open('d:\py\ProbabilityGrammar\\output.txt', 'w')
fw.write('The best answer of P = %f\n' % res)
outp('Building')
fw.close()
## open file "d:\py\ProbabilityGrammar\\output.txt"