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
    fo = open('input.txt', 'r')
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
        temp = temp.split()
        Grammar.append(temp)
        for j in xrange(2, len(temp) - 1, 2):
            Grammar[i][j] = eval(Grammar[i][j])
        Grammar[i][-1] = float(Grammar[i][-1])
    fo.close()


def progra(root):
    father = GrammarObj[root]
    if father in [1, 2, 4, 8]:
        return (1.0)
    res = 0
    for g in Grammar:
        if g[0] == root:
            temp = g[-1]
            for i in range(1, len(g) - 1, 2):
                # if not isinstance(g[i],str) : break
                Name = g[i]
                Proba = progra(Name)
                temp *= Proba
            if (temp > res):
                res, bes = temp, g
    # print '%s(%d) = %s(%d) + %s(%d)\n P = %f'%(root,father,left,lchild,right,rchild,res)
    BestRule[root] = bes
    return res


def Sum(a, b):
    return a + b


def GetTruePosition(root, NowCoodinate):
    father = GrammarObj[root]
    if father in [1, 2, 4, 8]:
        TruePosition[root] = NowCoodinate
        return
    g = BestRule[root]
    for i in range(1, len(g) - 1, 2):
        NewPosition = map(Sum, NowCoodinate, g[i + 1])
        GetTruePosition(g[i], NewPosition)


def PrintCombination(root):
    father = GrammarObj[root]
    if father in [1, 2, 4, 8]:
        return
    g = BestRule[root]
    fw.write('%s -> %s' % (root.center(CENTERWIDTH), g[1].center(CENTERWIDTH)))
    for i in range(3, len(g) - 1, 2):
        fw.write(' || %s' % g[i].center(CENTERWIDTH))
    fw.write('\n')
    for i in range(1, len(g) - 1, 2):
        PrintCombination(g[i])


class Vector3():
    def __init__(self, x, y, z):
        self.x, self.y, self.z = x, y, z

    def fprint(self, fo):
        fo.write('(%10f,%10f,%10f)' % (self.x, self.y, self.z))

    def sprint(self):
        print '(%f,%f,%f)' % (self.x, self.y, self.z)


def PrintTruePosition(TruePosition):
    fw.write('\nPosition of Each Object:\n')
    for i in TruePosition:
        Vec = Vector3(TruePosition[i][0], TruePosition[i][1], TruePosition[i][2])
        fw.write('%s:' % i.center(CENTERWIDTH))
        Vec.fprint(fw)
        fw.write('\n')


import fileinput
import re
import random
import os

os.chdir('d:\\py\\ProbabilityGrammar')
TruePosition = {}
GrammarObj = {}
Grammar = []
BestRule = {}
root = 'Building'
InputFile = 'inout.txt'
OutputFile = 'output.txt'
CENTERWIDTH = 15
init()
res = progra(root)
GetTruePosition(root, [29.409536, 39.305736, 44.277932, 0, 0, 0])
fw = open(OutputFile, 'w')
fw.write('The best answer of P = %f\n' % res)
fw.write('\nGrammar of Each Object:\n')
PrintCombination(root)
PrintTruePosition(TruePosition)
fw.close()
## open file "d:\py\ProbabilityGrammar\\output.txt"
