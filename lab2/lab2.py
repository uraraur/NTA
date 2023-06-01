import time
import signal
import sys
sys.path.insert(0, 'H:/ААА/NTA/lab2')
from lab import *

#Допоміжні функції

def gcd(a, b): 
    r_0, r_1 = a, b 
    u_0, u_1 = 1, 0
    v_0, v_1 = 0, 1

    while r_1 != 0:
        q = r_0 // r_1
        r_0, r_1 = r_1, r_0 - q*r_1
        u_0, u_1 = u_1, u_0 - q*u_1
        v_0, v_1 = v_1, v_0 - q*v_1

    return r_0, u_0, v_0

def inv(a, b):
    d, u, v = gcd(a, b)
    if d != 1:
        return "No inverse exists"
    return u   

def invpow(a, x, n): #обернене в якомусь степені))
    if x == 0:
        return 1
    b = a
    while x < -1:
        b = (b * a) % n
        x = x + 1  
    return inv(b, n) % n 

def chinese(X, canon): #КТО
    x = 0
    N = 1
    N_i = [0] * len(canon)
    M_i = [0] * len(canon)

    for i in range(len(canon)):
        N = N * canon[i]
    for i in range(len(canon)):
        N_i[i] = N // canon[i]     
        M_i[i] = inv(N_i[i], canon[i])

    for i in range(len(canon)):
        x = x + X[i] * N_i[i] * M_i[i] 
    x = x % N
    return x 

#-------------------------------------

#Повний перебір:

def brute_force_search(a, b, n):
    m = 0
    start_time = time.time()
    for i in range(n):
        m = pow(a, i, n)
        if m == b:
            return i
        end_time = time.time()
        if end_time - start_time > 295:
            return "Time out!!"
    return 0 

#-------------------------------------       

#Алгоритм Сільвера-Поліга-Гелльгама:

def pohlig_hellman_alg(a, b, n):
    start_time = time.time()
    ord = n - 1
    canon = canonical_search(ord)
    factors = []
    r = []
    for i in canon:
        if i not in factors:
            factors.append(i)
    powers = [0] * len(factors)

    for i in range(len(canon)):
        num = factors.index(canon[i])
        powers[num] = powers[num] + 1

    canon.clear()
    for i in range(len(factors)):
        canon.append(pow(factors[i],powers[i]))

    for p in factors:
        r_p = []
        for j in range(0, p):
            r_p.append(pow(a, (ord * j) // p, n ))
        r.append(r_p)

    end_time = time.time()
    if end_time - start_time > 295:
        return "Time out!!"

    X = []
    for i in range(len(factors)):
        num = pow(b, ord // factors[i], n)
        x_i = r[i].index(num)
        x_pow = x_i
        for j in range(1, powers[i]): 
            num = pow(b * invpow(a, -x_pow, n), ord // (factors[i] ** (j + 1)), n) 
            x_i = r[i].index(num)
            x_pow = (x_pow + x_i * (factors[i] ** j)) % canon[i]
        X.append(x_pow)

    return chinese(X, canon)


print(pohlig_hellman_alg(483303352902419, 511939775232752, 771816501687809))



