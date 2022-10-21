import numpy as np
S=[2,9,7,14,1,12,10,0,4,3,8,13,15,6,5,11]

def bin4(a):
    s=bin(a)[2:]
    while len(s)<4:
        s='0'+s
    x=[]
    for i in range(4):
        x.append(int(s[i]))
    return x

print("LAT")
LAT=np.zeros([16,16])
for i in range(16):
    for j in range(16):
        for k in range(16):
            a=k
            b=S[k]
            sum = 0
            for m in range(4):
                sum = sum + bin4(a)[m] * bin4(i)[m]
            for m in range(4):
                sum = sum + bin4(b)[m] * bin4(j)[m]
            if sum % 2 ==0:
                LAT[i][j]=LAT[i][j]+1
for i in range(16):
    for j in range(16):
        LAT[i][j] = LAT[i][j] - 8
print(LAT)
H=[]
NH=[]
PH=[]
for i in range(16):
    for j in range(16):
        if(LAT[i][j]!=0):
            H.append(bin4(i)+bin4(j))
            if(LAT[i][j]==8):
                p=[0,0]
            if(abs(LAT[i][j])==2):
                p=[1,0]
            if (abs(LAT[i][j])==4):
                p = [0, 1]
            PH.append(bin4(i)+bin4(j)+p)
        else:
            NH.append(bin4(i) + bin4(j))

print("linear pairs:")
print(H)
print("linear pairs whit correlation:")
print(PH)
