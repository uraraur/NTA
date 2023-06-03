from lab import *
import random
import math
import numpy as np

def precalc(a, n, S):
    A = []
    K = []
    while len(A) != len(S) + 5:
        k = random.randint(1, n - 1) 
        a_k = pow(a, k, n)
        canon = factor_probni_dilenya(a_k, S, [0] * len(S))
        if canon == 0:
            continue
        K.append(k)
        A.append(canon)
    A = np.array(A, dtype='object')
    K = np.array(K, dtype='object')
    return A, K

def solve_system(A, K, n):
    m = len(A[0])
    x = np.array([0] * m)
    k = len(A)
    c = 0
    pivot = A[0][0]
    f = np.vectorize(lambda a: math.gcd(a, n))
    for c in range(m):
        i, j = np.where(f(A[c:, c:]) == 1)
        p = i[0]
        q = j[0]

        pivot = A[p + c][q + c]
        inv = pow(pivot, -1, n)

        A[[c, p + c]] =  A[[p + c, c]]
        A[:, [c, q + c]] =  A[:, [q + c, c]]

        for i in range(c + 1, k):
            m_i = inv  * A[i, c]
            A[i, :] = (A[i, :] - A[c, :] * m_i) % n
            K[i] = (K[i] - K[c] * m_i) % n

        A[c, :] = A[c, :] * inv % n
        K[c] = K[c] * inv % n

    for i in range(m - 1, -1, -1):
        x[i] = (K[i] - (np.dot(A[i], x))) % n

    return x

#-------------------------------------

#Index-calculus:

def index_calculus(a, b, n):
    stableconst = 3.38 * np.exp(0.5 * np.sqrt(np.log(n) * np.log(np.log(n))))
    S = [2]
    for i in range (3, int(stableconst) + 1):
        if miller_rabin_primality(i, 10) == 1:
            S.append(i)
    A, K = precalc(a, n, S)
    print(A)
    print("------------")
    print(K)
    x = solve_system(A.copy(), K.copy(), n)
    print(x)
    canon = 0
    while canon == 0:
        k = random.randint(1, n - 1) 
        y = pow(a, k, n) * b % n
        canon = factor_probni_dilenya(y, S, [0] * len(S))
        print(k)
        print(canon)
    result = 0
    for i in range(len(canon)):
        if i != 0:
            result += canon[i] * x[i] 
    result = (result - k) % (n - 1)
    return result

print(index_calculus(10, 17, 47))
