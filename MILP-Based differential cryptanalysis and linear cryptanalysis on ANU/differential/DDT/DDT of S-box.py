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

print("DDT:")
DDT=np.zeros([16,16])
for i in range(16):
    for j in range(16):
        a=j
        b=i^j
        s=S[a]^S[b]
        DDT[i][s]=DDT[i][s]+1
print(DDT)
H=[]
NH=[]
PH=[]
for i in range(16):
    for j in range(16):
        if(DDT[i][j]!=0):
            H.append(bin4(i)+bin4(j))
            if(DDT[i][j]==16):
                p=[0,0]
            if(DDT[i][j]==2):
                p=[1,0]
            if (DDT[i][j]==4):
                p = [0, 1]
            PH.append(bin4(i)+bin4(j)+p)
        else:
            NH.append(bin4(i) + bin4(j))

print("differenre pairs:")
print(H)
print("differenre pairs whit probability:")
print(PH)

