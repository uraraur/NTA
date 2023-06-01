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
    canon = canonical_search(n)
    print(canon)
    factors = []
    for i in canon:
        factors.append(i)
    return 1

pohlig_hellman_alg(3, 13, 16)

print("HI")

