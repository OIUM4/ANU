from gurobipy import *

conv = []
inner = []

P = (
    20, 16, 28, 24, 17, 21, 25, 29,
    22, 18, 30, 26, 19, 23, 27, 31,
    11, 15,  3,  7, 14, 10,  6,  2,
     9, 13,  1,  5, 12,  8,  4,  0,
)


ROUND = 10
BanListlen = 0
act=0

def list_move_right(A,a):
    for i in range(a):
        A.insert(0,A.pop())
    return A

def list_move_left(A,a):
    for i in range(a):
        A.insert(len(A),A[0])
        A.remove(A[0])
    return A

def PrintOuter(BanList):
    opOuter = open("outer%d.lp"%ROUND, 'w+')
    opOuter.write("Minimize\n")
    buf = ''
    for i in range(0, ROUND):
        for j in range(0, 16):
            buf = buf + "a" + str(i) + "_" + str(j)
            if i != ROUND - 1 or j != 15:
                buf = buf + " + "
    opOuter.write(buf)
    opOuter.write('\n')

    opOuter.write("Subject to\n")
    a = [31 - x for x in range(32)]
    b = a.copy()
    y = list_move_right(a, 3)
    z = list_move_left(b, 8)
    for i in range(0, ROUND):
        for j in range(0, 8):
            buf = ''
            for k in range(0, 4):
                buf = buf + "x" + str(i) + "_" + str(4 * j + k)
                if k != 3:
                    buf = buf + " + "
            buf = buf + " - a" + str(i) + "_" + str(j) + " >= 0\n"
            for k in range(0, 4):
                buf = buf + "x" + str(i) + "_" + str(4 * j + k) + " - a" + str(i) + "_" + str(j) + " <= 0\n"

            for k in range(len(outer)):
                for l in range(9):
                    if outer[k][l] > 0:
                        if l <= 3:
                            buf = buf + " + " + str(outer[k][l]) + " y" + str(i) + "_" + str(4 * j + 3 - l)
                        if 4 <= l and l <= 7:
                            buf = buf + " + " + str(outer[k][l]) + " x" + str(i) + "_" + str(4 * j + 7 - l)
                        if l == 8:
                            buf = buf + " >= -" + str(outer[k][l]) + "\n"
                    if outer[k][l] < 0:
                        if l <= 3:
                            buf = buf + " - " + str(-outer[k][l]) + " y" + str(i) + "_" + str(4 * j + 3 - l)
                        if 4 <= l and l <= 7:
                            buf = buf + " - " + str(-outer[k][l]) + " x" + str(i) + "_" + str(4 * j + 7 - l)
                        if l == 8:
                            buf = buf + " >= " + str(-outer[k][l]) + "\n"
                    if outer[k][l] == 0:
                        if l == 8:
                            buf = buf + " >= " + str(outer[k][l]) + "\n"
            opOuter.write(buf)

        for j in range(0, 8):
            buf = ''
            for k in range(0, 4):
                buf = buf + "x" + str(i) + "_" + str(4 * j + k)
                if k != 3:
                    buf = buf + " + "
            buf = buf + " - a" + str(i) + "_" + str(j + 8) + " >= 0\n"
            for k in range(0, 4):
                buf = buf + "x" + str(i) + "_" + str(4 * j + k) + " - a" + str(i) + "_" + str(j + 8) + " <= 0\n"

            for k in range(len(outer)):
                for l in range(9):
                    if outer[k][l] > 0:
                        if l <= 3:
                            buf = buf + " + " + str(outer[k][l]) + " z" + str(i) + "_" + str(4 * j + 3 - l)
                        if 4 <= l and l <= 7:
                            buf = buf + " + " + str(outer[k][l]) + " x" + str(i) + "_" + str(4 * j + 7 - l)
                        if l == 8:
                            buf = buf + " >= -" + str(outer[k][l]) + "\n"
                    if outer[k][l] < 0:
                        if l <= 3:
                            buf = buf + " - " + str(-outer[k][l]) + " z" + str(i) + "_" + str(4 * j + 3 - l)
                        if 4 <= l and l <= 7:
                            buf = buf + " - " + str(-outer[k][l]) + " x" + str(i) + "_" + str(4 * j + 7 - l)
                        if l == 8:
                            buf = buf + " >= " + str(-outer[k][l]) + "\n"
                    if outer[k][l] == 0:
                        if l == 8:
                            buf = buf + " >= " + str(outer[k][l]) + "\n"
            opOuter.write(buf)

        buf = ''
        for j in range(0, 32):
            buf = buf + " x" + str(i) + "_" + str(j) + " - " + " x" + str(i + 1) + "_" + str(P[j] + 32) + " = 0\n"
        opOuter.write(buf)

        buf = ''
        for j in range(0, 32):
            for k in range(2**3):
                sum = 0
                if (k & 1 == 1):
                    buf = buf + " + "
                    sum = sum + 1
                else:
                    buf = buf + " - "
                buf = buf + "y" + str(i) + "_" + str(y[31 - j])
                if (k & 2 == 2):
                    buf = buf + " + "
                    sum = sum + 1
                else:
                    buf = buf + " - "
                buf = buf + "z" + str(i) + "_" + str(z[31 - j])
                if (k & 4 == 4):
                    buf = buf + " + "
                    sum = sum + 1
                else:
                    buf = buf + " - "
                buf = buf + "x" + str(i + 1) + "_" + str(P[j])
                if (sum % 2 == 0):
                    buf = buf + " + "
                    sum = sum + 1
                else:
                    buf = buf + " - "
                buf = buf + "x" + str(i) + "_" + str(j + 32)
                buf = buf + " <= " + str(sum - 1) + "\n"
        opOuter.write(buf)

    buf = ''
    for i in range(0, 32):
        buf = buf + "x0_" + str(i)
        if i != 31:
            buf = buf + " + "
        if i == 31:
            buf = buf + " >= 1\n"
    opOuter.write(buf)

    buf = ''
    for i in BanList:
        for j in range(0, len(i)):
            buf = buf + "a" + str(i[j][0]) + "_" + str(i[j][1])
            if j != len(i) - 1:
                buf = buf + " + "
            else:
                buf = buf + " <= " + str(len(i) - 1) + '\n'
    opOuter.write(buf)

    opOuter.write("Binary\n")
    for i in range(0, ROUND):
        buf = ''
        for j in range(0, 16):
            buf = buf + "a" + str(i) + "_" + str(j) + "\n"
        opOuter.write(buf)
    for i in range(0, ROUND + 1):
        buf = ''
        for j in range(0, 64):
            buf = buf + "x" + str(i) + "_" + str(j) + "\n"
        opOuter.write(buf)
    for i in range(0, ROUND):
        buf = ''
        for j in range(0, 32):
            buf = buf + "y" + str(i) + "_" + str(j) + "\n"
            buf = buf + "z" + str(i) + "_" + str(j) + "\n"
        opOuter.write(buf)
    opOuter.close()

def PrintInner(SolveList):
    opInner = open("inner%d.lp"%ROUND, "w+")

    opInner.write("Minimize\n")
    buf = ''
    for i in range(0, len(SolveList)):
        buf = buf + "2 p" + str(SolveList[i][0]) + "_" + str(SolveList[i][1]) + "_0 + 1 p" + str(SolveList[i][0]) + "_" + str(SolveList[i][1]) + "_1"
        if i != len(SolveList) - 1:
            buf = buf + " + "
        else:
            buf = buf + "\n"
    opInner.write(buf)

    opInner.write("Subject to\n")
    for i in range(0, len(SolveList)):
        buf = ''
        if SolveList[i][1] <= 7:
            for k in range(0, 4):
                buf = buf + "4 y" + str(SolveList[i][0]) + "_" + str(4 * SolveList[i][1] + 3 - k)
                if k != 3:
                    buf = buf + " + "
            for k in range(0, 4):
                buf = buf + " - x" + str(SolveList[i][0]) + "_" + str(4 * SolveList[i][1] + 3 - k)
            buf = buf + " >= 0\n"

            for k in range(0, 4):
                buf = buf + "4 x" + str(SolveList[i][0]) + "_" + str(4 * SolveList[i][1] + 3 - k)
                if k != 3:
                    buf = buf + " + "
            for k in range(0, 4):
                buf = buf + " - y" + str(SolveList[i][0]) + "_" + str(4 * SolveList[i][1] + 3 - k)
            buf = buf + " >= 0\n"

        if SolveList[i][1] >= 8:
            for k in range(0, 4):
                buf = buf + "4 z" + str(SolveList[i][0]) + "_" + str(4 * (SolveList[i][1] - 8) + 3 - k)
                if k != 3:
                    buf = buf + " + "
            for k in range(0, 4):
                buf = buf + " - x" + str(SolveList[i][0]) + "_" + str(4 * (SolveList[i][1] - 8) + 3 - k)
            buf = buf + " >= 0\n"

            for k in range(0, 4):
                buf = buf + "4 x" + str(SolveList[i][0]) + "_" + str(4 * (SolveList[i][1] - 8) + 3 - k)
                if k != 3:
                    buf = buf + " + "
            for k in range(0, 4):
                buf = buf + " - z" + str(SolveList[i][0]) + "_" + str(4*(SolveList[i][1] - 8) + 3 - k)
            buf = buf + " >= 0\n"
        opInner.write(buf)

        buf = ''
        for k in range(0, len(inner)):
            for l in range(0, 11):
                if inner[k][l] > 0:
                    if l <= 3:
                        if SolveList[i][1] <= 7:
                            buf = buf + " + " + str(inner[k][l]) + " y" + str(SolveList[i][0]) + "_" + str(4 * SolveList[i][1] + 3 - l)
                        if SolveList[i][1] >= 8:
                            buf = buf + " + " + str(inner[k][l]) + " z" + str(SolveList[i][0]) + "_" + str(4 * (SolveList[i][1]-8) + 3 - l)
                    if 4 <= l and l <= 7:
                        if SolveList[i][1] <= 7:
                            buf = buf + " + " + str(inner[k][l]) + " x" + str(SolveList[i][0]) + "_" + str(4 * SolveList[i][1] + 7 - l)
                        if SolveList[i][1] >= 8:
                            buf = buf + " + " + str(inner[k][l]) + " x" + str(SolveList[i][0]) + "_" + str(4 * (SolveList[i][1]-8) + 7 - l)
                    if 8 <= l and l <= 9:
                        buf = buf + " + " + str(inner[k][l]) + " p" + str(SolveList[i][0]) + "_" + str(SolveList[i][1]) + "_" + str(l - 8)
                    if l == 10:
                        buf = buf + " >= -" + str(inner[k][l]) + "\n"
                if inner[k][l] < 0:
                    if l <= 3:
                        if SolveList[i][1] <= 7:
                            buf = buf + " - " + str(-inner[k][l]) + " y" + str(SolveList[i][0]) + "_" + str(4 * SolveList[i][1] + 3 - l)
                        if SolveList[i][1] >= 8:
                            buf = buf + " - " + str(-inner[k][l]) + " z" + str(SolveList[i][0]) + "_" + str(4 * (SolveList[i][1]-8) + 7 - l)
                    if 4 <= l and l <= 7:
                        if SolveList[i][1] <= 7:
                            buf = buf + " - " + str(-inner[k][l]) + " x" + str(SolveList[i][0]) + "_" + str(4 * SolveList[i][1] + 7 - l)
                        if SolveList[i][1] >= 8:
                            buf = buf + " - " + str(-inner[k][l]) + " x" + str(SolveList[i][0]) + "_" + str(4 * (SolveList[i][1]-8) + 7 - l)
                    if 8 <= l and l <= 9:
                        buf = buf + " - " + str(-inner[k][l]) + " p" + str(SolveList[i][0]) + "_" + str(SolveList[i][1]) + "_" + str(l - 8)
                    if l == 10:
                        buf = buf + " >= " + str(-inner[k][l]) + "\n"
                if inner[k][l] == 0:
                    if l == 10:
                        buf = buf + " >= " + str(inner[k][l]) + "\n"
        opInner.write(buf)

    a = [31 - x for x in range(32)]
    b = a.copy()
    y = list_move_right(a, 3)
    z = list_move_left(b, 8)
    for i in range(0, ROUND):
        buf = ''
        sl = []
        sl.append(i)
        for j in range(0, 16):
            sl.append(j)
            if sl not in SolveList and j <= 7:
                for k in range(0, 4):
                    buf = buf + " x" + str(i) + "_" + str(4 * j + k) + " = 0\n"
                    buf = buf + " y" + str(i) + "_" + str(4 * j + k) + " = 0\n"
            if sl not in SolveList and j >= 8:
                for k in range(0, 4):
                    buf = buf + " x" + str(i) + "_" + str(4 * (j-8) + k) + " = 0\n"
                    buf = buf + " z" + str(i) + "_" + str(4 * (j-8) + k) + " = 0\n"
            sl.pop()
        opInner.write(buf)

        buf = ''
        for j in range(0, 32):
            buf = buf + " x" + str(i) + "_" + str(j) + " - " + " x" + str(i + 1) + "_" + str(P[j] + 32) + " = 0\n"
        opInner.write(buf)

        buf = ''
        for j in range(0, 32):
            for k in range(2 ** 3):
                sum = 0
                if (k & 1 == 1):
                    buf = buf + " + "
                    sum = sum + 1
                else:
                    buf = buf + " - "
                buf = buf + "y" + str(i) + "_" + str(y[31 - j])
                if (k & 2 == 2):
                    buf = buf + " + "
                    sum = sum + 1
                else:
                    buf = buf + " - "
                buf = buf + "z" + str(i) + "_" + str(z[31 - j])
                if (k & 4 == 4):
                    buf = buf + " + "
                    sum = sum + 1
                else:
                    buf = buf + " - "
                buf = buf + "x" + str(i + 1) + "_" + str(P[j])
                if (sum % 2 == 0):
                    buf = buf + " + "
                    sum = sum + 1
                else:
                    buf = buf + " - "
                buf = buf + "x" + str(i) + "_" + str(j + 32)
                buf = buf + " <= " + str(sum - 1) + "\n"
        opInner.write(buf)

    buf = ''
    for i in SolveList:
            for j in range(4):
                buf= buf + " + " + "x" + str(i[0]) + "_" + str(4 * (i[1]%8) + j)
            buf = buf + " >= 1\n"
    opInner.write(buf)

    opInner.write("Binary\n")
    for i in range(0, ROUND+1):
        buf = ''
        for j in range(0, 64):
            buf = buf + "x" + str(i) + "_" + str(j) + "\n"
        opInner.write(buf)
    for i in range(0, ROUND):
        buf = ''
        for j in range(0, 32):
            buf = buf + "y" + str(i) + "_" + str(j) + "\n"
            buf = buf + "z" + str(i) + "_" + str(j) + "\n"
        opInner.write(buf)
    buf = ''
    for i in range(0, len(SolveList)):
        buf = buf + "p" + str(SolveList[i][0]) + "_" + str(SolveList[i][1]) + "_0\n"
        buf = buf + "p" + str(SolveList[i][0]) + "_" + str(SolveList[i][1]) + "_1\n"
    opInner.write(buf)
    opInner.close()

def strtoint(s):
    reg = 0
    s1 = ''
    s2 = ''
    result = []
    for i in range(0, len(s)):
        if s[i] == '_':
            reg = 1
        if s[i] >= '0' and s[i] <= '9':
            if reg == 0:
                s1 = s1 + s[i]
            if reg == 1:
                s2 = s2 + s[i]

    result.append(int(s1))
    result.append(int(s2))
    return result

with open('linear/Inequalities of S-box/fina_outer.txt',) as f:
    for line in f.readlines():
         temp=line.split()
         for i in range(len(temp)):
             temp[i] = int(temp[i])
         outer.append(temp)
with open('linear/Inequalities of S-box/fina_inner.txt',) as f:
    for line in f.readlines():
         temp=line.split()
         for i in range(len(temp)):
             temp[i] = int(temp[i])
         inner.append(temp)

BanList = []
bl = []
blstring = []
resreg = 32
filename = "result_" + str(ROUND) + ".txt"
opResult = open(filename,'w+')

while True:
    PrintOuter(BanList)

    o = read("outer%d.lp"%ROUND)
    o.Params.MIPfocus=2
    o.Params.TimeLimit = 10000.0
    o.optimize()
    obj = o.getObjective()
    if act==0: act=obj.getValue()
    if act == 0 or (act != 0 and obj.getValue() < act + 5):
        bl = []
        blstring = []
        for v in o.getVars():
            if v.x == 1 and v.VarName[0] == 'a':
                blstring.append(v.VarName)
        for b in blstring:
            bl.append(strtoint(b))
        BanList.append(bl)
        BanListlen = len(bl)
        print(bl)
        PrintInner(bl)

        i = read("inner%d.lp"%ROUND)
        i.Params.MIPfocus=2
        i.Params.TimeLimit = 40000.0
        i.optimize()
#        i.computeIIS()
#        i.write("model1.ilp")
        buf = ''
        buf = buf + str(bl) + " " + str(i.getObjective().getValue()) + "\n"
        for v in i.getVars():
            if v.x == 1:
                buf = buf + v.VarName + " "
        buf = buf + "\n"
        opResult.write(buf)
        opResult.flush()
    else:
        break

# print len(BanList)
