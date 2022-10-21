from gurobipy import *

def B1(a,i):
    answers=[ele for ele in a]
    answers[i]=(answers[i]+1)%2
    return answers

def list_union(a,b):
    answers=[ele for ele in a]
    for ele in b:
        if ele not in a:
            answers.append(ele)
    return answers

def list_difference(a,b):
    answers=[ele for ele in a]
    for ele in b:
        if ele  in a:
            answers.remove(ele)
    return answers

def list_intersection(a,b):
    answers=[]
    for ele in b:
        if ele  in a:
            answers.append(ele)
    return answers

def expand1(apoints,n):
    OUT = []
    for a in apoints:
        s = []
        S = []
        U = []
        for i in range(n + 1):
            S.append([])
            U.append([])

        for b in apoints:
            u = [(int(a[i]) + int(b[i])) % 2 for i in range(n)]
            sum = 0
            w = 0
            for i in range(n):
                sum = sum + int(a[i]) * int(u[i])
                w = w + int(u[i])
            if sum == 0:
                if u not in U[w]: U[w].append(u)

        if len(U[1]) == 0:
            for x in U[0]:
                OUT.append([a, x])
            continue
        else:
            for x in U[1]:
                s.append([a, x])

        for x in U[0]:
            S[0].append([a, x])
        for x in U[1]:
            S[1].append([a, x])

        k = 2
        while k <= n:
            if len(U[k]) == 0:
                k = k + 1
                break
            for u in U[k]:
                o = 1
                for i in range(n):
                    v = u.copy()
                    if u[i] == 1:
                        v[i] = 0
                        if [a, v] not in S[k - 1]:
                            o = 0
                            break
                if o == 1:
                    S[k].append([a, u])
                    for i in range(n):
                        v = u.copy()
                        if u[i] == 1:
                            v[i] = 0
                            if [a, v] in s: s.remove([a, v])
            for x in S[k]:
                s.append(x)
            k = k + 1
        for x in s:
            OUT.append(x)
    inequality = []
    for x in OUT:
        sum = 0
        c = []
        for i, j in zip(x[0], x[1]):
            sum = sum + int(i)
            if int(i) == 1:
                c.append(-1)
            else:
                if int(j) == 0:
                    c.append(1)
                else:
                    c.append(0)
        c.append(sum - 1)
        inequality.append(c)
    return inequality

def expand2(apoints,n):
    C = []
    near = []
    for a in apoints:
        near_a = []
        for b in apoints:
            if a != b:
                sum = 0
                for i in range(n):
                    sum = sum + (a[i] + b[i]) % 2
                if sum == 1: near_a.append(b)
        near.append(near_a)
    for a, x in zip(apoints, near):
        if len(x) >= 2:
            i = 0
            while i < len(x):
                j = i + 1
                m = 0
                while j < len(x):
                    if m == 0:
                        b = x[i]
                        c = x[j]
                    else:
                        b = x[j]
                        c = x[i]
                    d = [(a[k] + b[k] + c[k]) % 2 for k in range(n)]
                    if d in apoints:
                        Ba = list_union([B1(a, k) for k in range(n)], [a])
                        Bb = list_union([B1(b, k) for k in range(n)], [b])
                        Bc = list_union([B1(c, k) for k in range(n)], [c])
                        Pa = list_difference(Ba, apoints)
                        Ra = list_union(Pa, [c])
                        Pb = list_difference(Bb, apoints)
                        Rb = [k for k in Pb]
                        Rc = list_difference(Bc, apoints)
                        for p in Pa:
                            e = [(p[k] + a[k] + b[k]) % 2 for k in range(n)]
                            Rb = list_union(Rb, [e])
                            e = [(p[k] + a[k] + c[k]) % 2 for k in range(n)]
                            Rc = list_union(Rc, [e])
                        for p in Pb:
                            e = [(p[k] + b[k] + c[k]) % 2 for k in range(n)]
                            Rc = list_union(Rc, [e])
                        Q = list_union(list_union(Pa, Rb), Rc)
                        na = [0] * (n + 1)
                        nb = [0] * (n + 1)
                        nc = [0] * (n + 1)
                        for k in range(n):
                            if (c[k] + a[k]) % 2 == 1:
                                t = 2
                            else:
                                t = 1
                                for q in list_intersection(Q, Ba):
                                    if (q[k] + a[k]) % 2 == 1:
                                        t = 2
                                        break
                            na[k] = na[k] + t * (1 - 2 * a[k])
                            na[n] = na[n] + t * a[k]
                            t = 1
                            for q in list_intersection(Q, Bb):
                                if (q[k] + b[k]) % 2 == 1:
                                    t = 2
                                    break
                            nb[k] = nb[k] + t * (1 - 2 * b[k])
                            nb[n] = nb[n] + t * b[k]
                            t = 1
                            for q in list_intersection(Q, Bc):
                                if (q[k] + c[k]) % 2 == 1:
                                    t = 2
                                    break
                            nc[k] = nc[k] + t * (1 - 2 * c[k])
                            nc[n] = nc[n] + t * c[k]
                        new = [na[k] + nb[k] + nc[k] for k in range(n + 1)]
                        new[n] = new[n] - 8
                        C = list_union(C, [new])
                    if m == 1: j = j + 1
                    m = (m + 1) % 2
                i = i + 1
    return C

def expand3(apoints,n):
    C=[]
    for a in apoints:
        B = list_union([B1(a, k) for k in range(n)], [a])
        Q = list_difference(B, apoints)
        new = [0] * (n + 1)
        for k in range(n):
            t = 1
            for q in Q:
                if (q[k] + a[k]) % 2 == 1:
                    t = 2
                    break
            new[k] = new[k] + t * (1 - 2 * a[k])
            new[n] = new[n] + t * a[k]
        new[n] = new[n] - 2
        C.append(new)
    return C

# point : linear pairs or linear pairs whit correlation
points=[[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 1, 0, 1], [0, 0, 0, 1, 0, 1, 1, 1], [0, 0, 0, 1, 1, 0, 0, 0], [0, 0, 0, 1, 1, 0, 0, 1], [0, 0, 0, 1, 1, 0, 1, 0], [0, 0, 0, 1, 1, 0, 1, 1], [0, 0, 0, 1, 1, 1, 0, 0], [0, 0, 0, 1, 1, 1, 0, 1], [0, 0, 0, 1, 1, 1, 1, 0], [0, 0, 0, 1, 1, 1, 1, 1], [0, 0, 1, 0, 0, 1, 0, 1], [0, 0, 1, 0, 0, 1, 1, 1], [0, 0, 1, 0, 1, 0, 0, 0], [0, 0, 1, 0, 1, 0, 0, 1], [0, 0, 1, 0, 1, 0, 1, 0], [0, 0, 1, 0, 1, 0, 1, 1], [0, 0, 1, 0, 1, 1, 0, 0], [0, 0, 1, 0, 1, 1, 0, 1], [0, 0, 1, 0, 1, 1, 1, 0], [0, 0, 1, 0, 1, 1, 1, 1], [0, 0, 1, 1, 1, 0, 0, 1], [0, 0, 1, 1, 1, 0, 1, 0], [0, 0, 1, 1, 1, 1, 0, 0], [0, 0, 1, 1, 1, 1, 1, 1], [0, 1, 0, 0, 1, 0, 1, 0], [0, 1, 0, 0, 1, 0, 1, 1], [0, 1, 0, 0, 1, 1, 1, 0], [0, 1, 0, 0, 1, 1, 1, 1], [0, 1, 0, 1, 0, 0, 0, 1], [0, 1, 0, 1, 0, 0, 1, 1], [0, 1, 0, 1, 1, 0, 0, 0], [0, 1, 0, 1, 1, 0, 0, 1], [0, 1, 0, 1, 1, 0, 1, 0], [0, 1, 0, 1, 1, 0, 1, 1], [0, 1, 0, 1, 1, 1, 0, 0], [0, 1, 0, 1, 1, 1, 0, 1], [0, 1, 0, 1, 1, 1, 1, 0], [0, 1, 0, 1, 1, 1, 1, 1], [0, 1, 1, 0, 0, 1, 0, 0], [0, 1, 1, 0, 0, 1, 1, 0], [0, 1, 1, 0, 1, 0, 0, 0], [0, 1, 1, 0, 1, 0, 0, 1], [0, 1, 1, 0, 1, 0, 1, 0], [0, 1, 1, 0, 1, 0, 1, 1], [0, 1, 1, 0, 1, 1, 0, 0], [0, 1, 1, 0, 1, 1, 0, 1], [0, 1, 1, 0, 1, 1, 1, 0], [0, 1, 1, 0, 1, 1, 1, 1], [0, 1, 1, 1, 0, 0, 0, 1], [0, 1, 1, 1, 0, 0, 1, 1], [0, 1, 1, 1, 0, 1, 0, 0], [0, 1, 1, 1, 0, 1, 1, 0], [1, 0, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 1, 1], [1, 0, 0, 0, 0, 1, 0, 0], [1, 0, 0, 0, 0, 1, 1, 0], [1, 0, 0, 0, 0, 1, 1, 1], [1, 0, 0, 0, 1, 0, 0, 1], [1, 0, 0, 0, 1, 0, 1, 1], [1, 0, 0, 0, 1, 1, 0, 0], [1, 0, 0, 0, 1, 1, 0, 1], [1, 0, 0, 0, 1, 1, 1, 0], [1, 0, 0, 1, 0, 0, 0, 1], [1, 0, 0, 1, 0, 0, 1, 0], [1, 0, 0, 1, 0, 0, 1, 1], [1, 0, 0, 1, 0, 1, 0, 0], [1, 0, 0, 1, 0, 1, 1, 0], [1, 0, 0, 1, 1, 0, 0, 0], [1, 0, 0, 1, 1, 0, 1, 0], [1, 0, 0, 1, 1, 1, 0, 1], [1, 0, 0, 1, 1, 1, 1, 0], [1, 0, 0, 1, 1, 1, 1, 1], [1, 0, 1, 0, 0, 0, 0, 1], [1, 0, 1, 0, 0, 0, 1, 0], [1, 0, 1, 0, 0, 0, 1, 1], [1, 0, 1, 0, 0, 1, 0, 0], [1, 0, 1, 0, 0, 1, 1, 0], [1, 0, 1, 0, 1, 0, 0, 0], [1, 0, 1, 0, 1, 0, 1, 0], [1, 0, 1, 0, 1, 0, 1, 1], [1, 0, 1, 0, 1, 1, 0, 1], [1, 0, 1, 0, 1, 1, 1, 1], [1, 0, 1, 1, 0, 0, 0, 1], [1, 0, 1, 1, 0, 0, 1, 1], [1, 0, 1, 1, 0, 1, 0, 0], [1, 0, 1, 1, 0, 1, 1, 0], [1, 0, 1, 1, 0, 1, 1, 1], [1, 0, 1, 1, 1, 0, 0, 0], [1, 0, 1, 1, 1, 0, 0, 1], [1, 0, 1, 1, 1, 0, 1, 1], [1, 0, 1, 1, 1, 1, 0, 0], [1, 0, 1, 1, 1, 1, 1, 0], [1, 1, 0, 0, 0, 0, 0, 1], [1, 1, 0, 0, 0, 0, 1, 0], [1, 1, 0, 0, 0, 0, 1, 1], [1, 1, 0, 0, 0, 1, 0, 0], [1, 1, 0, 0, 0, 1, 1, 0], [1, 1, 0, 0, 1, 0, 0, 1], [1, 1, 0, 0, 1, 0, 1, 1], [1, 1, 0, 0, 1, 1, 0, 0], [1, 1, 0, 0, 1, 1, 0, 1], [1, 1, 0, 0, 1, 1, 1, 0], [1, 1, 0, 1, 0, 0, 0, 1], [1, 1, 0, 1, 0, 0, 1, 1], [1, 1, 0, 1, 0, 1, 0, 0], [1, 1, 0, 1, 0, 1, 0, 1], [1, 1, 0, 1, 0, 1, 1, 0], [1, 1, 0, 1, 1, 0, 0, 0], [1, 1, 0, 1, 1, 0, 1, 0], [1, 1, 0, 1, 1, 1, 0, 0], [1, 1, 0, 1, 1, 1, 0, 1], [1, 1, 0, 1, 1, 1, 1, 1], [1, 1, 1, 0, 0, 0, 0, 1], [1, 1, 1, 0, 0, 0, 1, 1], [1, 1, 1, 0, 0, 1, 0, 0], [1, 1, 1, 0, 0, 1, 0, 1], [1, 1, 1, 0, 0, 1, 1, 0], [1, 1, 1, 0, 1, 0, 0, 0], [1, 1, 1, 0, 1, 0, 0, 1], [1, 1, 1, 0, 1, 0, 1, 0], [1, 1, 1, 0, 1, 1, 0, 1], [1, 1, 1, 0, 1, 1, 1, 1], [1, 1, 1, 1, 0, 0, 0, 1], [1, 1, 1, 1, 0, 0, 1, 0], [1, 1, 1, 1, 0, 0, 1, 1], [1, 1, 1, 1, 0, 1, 0, 0], [1, 1, 1, 1, 0, 1, 1, 0], [1, 1, 1, 1, 1, 0, 0, 0], [1, 1, 1, 1, 1, 0, 0, 1], [1, 1, 1, 1, 1, 0, 1, 1], [1, 1, 1, 1, 1, 1, 0, 0], [1, 1, 1, 1, 1, 1, 1, 0]]

n=len(points[0])
apoints = []
for i in range(2**n):
    a=[]
    for j in bin(i)[2:]:
        a.append(int(j))
    while(len(a)<n):
        a=[0]+a
    if a not in points:
        apoints.append(a)

inequalitys=[]
with open('init_outer.txt','r') as f:
    for line in f.readlines():
         temp=line.split()
         for i in range(len(temp)):
             temp[i] = int(temp[i])
         inequalitys.append(temp)
inequalitys = list_union(expand1(apoints, n), inequalitys)
inequalitys = list_union(expand2(apoints, n), inequalitys)
inequalitys = list_union(expand3(apoints, n), inequalitys)
add = []
for x in apoints:
    c = []
    for i in range(len(inequalitys)):
        sum = 0
        for j in range(n):
            sum = sum + x[j] * inequalitys[i][j]
        sum = sum + inequalitys[i][n]
        if sum < 0: c.append(i)
    add.append(c)
z = []
a = len(inequalitys)
for x in range(a):
    z.append('z%d' % x)

try:

    # Create a new model
    model = Model("mip1")

    # Create variables
    for i in range(a):
        z[i] = model.addVar(vtype=GRB.BINARY, name='z%d' % i)

    # Set objective
    sum = 0
    for x in z:
        sum = sum + x
    model.setObjective(sum, GRB.MINIMIZE)

    # Add constraint:
    for x in add:
        sum = 0
        for y in x:
            sum = sum + z[y]
        model.addConstr(sum >= 1, "c")
    del (add)

    model.optimize()

    with open('fina_outer.txt', 'w') as h:
        for v in model.getVars():
            if v.x == 1.0:
                a = int(v.varName[1:])
                for x in inequalitys[a]:
                    h.write(str(x) + ' ')
                h.write('\n')

    print('Obj:', model.objVal)

except GurobiError:
    print('Error reported')



