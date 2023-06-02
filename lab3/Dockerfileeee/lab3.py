from lab import *
import random
import math
import numpy as np


#-------------------------------------

#Index-calculus:

def index_calculus(a, b, n):
    stableconst = 3.38 * np.exp(0.5 * np.sqrt(np.log(n) * np.log(np.log(n))))
    S = [2]
    for i in range (3, int(stableconst) + 1):
        if miller_rabin_primality(i, 10) == 1:
            S.append(i)
    print(S)
    A = []
    K = []
    while np.linalg.matrix_rank(A) != len(S):
        k = random.randint(1, n - 1) 
        print(k)
        a_k = pow(a, k, n)
        print(a_k)
        canon = factor_probni_dilenya(a_k, S, [0] * len(S))
        print(canon)
        if canon == 0:
            continue
        K.append(k)
        A.append(canon)
        print(A)
        print(K)

    x = np.linalg.solve(A, K)
    print(x)
    
    return 1

print(index_calculus(10, 17, 47))