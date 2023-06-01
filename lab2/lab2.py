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

def invpow(a, x, n):
    if x == 0:
        return 1
    b = a
    while x < -1:
        b = (b * a) % n
        x = x + 1  
    return inv(b, n) % n 

#-------------------------------------
#Повний перебір:

def brute_force_search(a, b, n):
    m = 0
    start_time = time.time()
    for i in range(n):
        m = pow(a, i) % n
        if m == b:
            return i
        end_time = time.time()
        if end_time - start_time > 295:
            return "Time out!!"
    return 0 

#-------------------------------------       
#Алгоритм Сільвера-Поліга-Гелльгама:

def pohlig_hellman_alg(a, b, n):
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

    for p in factors:
        r_p = []
        for j in range(0, p):
            r_p.append(pow(a, (ord * j) // p) % n )
        r.append(r_p)

    print(f"canon: {canon}, {factors}, {powers}")
    print(r)
    X = []
    for i in range(len(factors)):
        num = pow(b, ord // factors[i]) % n
        x_i = r[i].index(num)
        x_pow = x_i
        for j in range(1, powers[i]): 
            num = pow(b * invpow(a, -x_pow, n), ord // (factors[i] ** (j + 1)))  % n
            x_i = r[i].index(num)
            x_pow = x_pow + x_i * (factors[i] ** j)
        X.append(x_pow) #########
    print(X)

    return 1

pohlig_hellman_alg(5, 11, 97)

print("HI")

