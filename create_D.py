#tworznie zależności
def d1(A,B):
    return A[0] == 'A' and B[0] == 'B' and A[1] == B[1] and A[2] == B[3]

def d2(B,C):
    return B[0] == 'B' and C[0] == 'C' and B[1] == C[1] and B[2] == C[2] and B[3] == C[3]

def d3(C,A):
    return C[0] == 'C' and A[0] == 'A' and C[2] == A[1] and (C[3] == A[1] or C[3] == A[2])

def d4(C,B):
    return C[0] == 'C' and B[0] ==  'B' and C[2] == B[2] and B[1] == C[3]

def d5(C1,C2):
    return C1[0] == 'C' and C2[0] == 'C' and  C1[2] == C2[2] and C1[3] == C2[3]
    
#dodatkowe warunki zapobiegające nadmiarowym krawędziom
def d3_prim(C,A):
    return C[1] == A[1] - 1

def d4_prim(C,B):
    return C[1] == B[1] - 1 and B[2] != B[1]

def d5_prim(C1,C2):
    return C1[1] == C2[1] - 1 and C2[1] != C2[2]

def create_D(sigma):
    e = len(sigma)
    D = []
    D_prim = []
    I = []
    for i in range(e):
        for j in range(i+1,e):
            operation1 = sigma[i]
            operation2 = sigma[j]

            flag = True

            if d1(operation1,operation2):
                D.append([operation1,operation2])
                D_prim.append([operation1,operation2])
                flag = False

            if d2(operation1,operation2):
                D.append([operation1,operation2])
                D_prim.append([operation1,operation2])
                flag = False
                
            if d3(operation1,operation2):
                D.append([operation1,operation2])
                if d3_prim(operation1,operation2):
                    D_prim.append([operation1,operation2])
                flag = False

            if d4(operation1,operation2):
                D.append([operation1,operation2])
                if d4_prim(operation1,operation2):
                    D_prim.append([operation1,operation2])
                flag = False

            if d5(operation1,operation2):
                D.append([operation1,operation2])
                if d5_prim(operation1,operation2):
                    D_prim.append([operation1,operation2])
                flag = False
            
            if flag:
                I.append([operation1, operation2])

    return D_prim,D,I
            
            






