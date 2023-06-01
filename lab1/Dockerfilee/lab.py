import random
import math
import time
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 

prime = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]

#Iмовiрнiсний тест Мiллера-Рабiна та допоміжна функція перевірки числа на псевдопростоту:

def pseudo_prime(x, d, p, s):
    if pow(x, d, p) == 1 or pow(x, d, p) == -1 % p:
        return 1
    x_r = pow(x, 2 * d, p) 
    for i in range(1, s):
        if x_r == -1 % p:
            return 1
        if x_r == 1:
            return 0
        x_r = x_r ** 2 % p
    return 0

def miller_rabin_primality(p, k):
    j = 1
    while j < k:
        if p % 2 == 0:
            return (f"The number {p} is composite")
        n = p - 1
        s = 0
        while n % 2 == 0:
            n = n // 2
            s = s + 1
        x = random.randint(2, p - 1)
        if math.gcd(x, p) > 1:
            return (f"The number {p} is composite")
        if pseudo_prime(x, n, p, s) == 0:
            return (f"The number {p} is composite")
        j = j + 1
    return 1

#Метод пробних ділень:

def probni_dilenya(n): # n = a_t * 10^t + a_(t-1) * 10^(t-1) + ... + a_1 * 10 + a0 * 1
    n_string = str(n)
    b = []
    for i in n_string[::-1]:
        b.append(int(i))
    
    for m in prime[0:15]:
        r = [0] * len(b)
        r[0] = 1
        for i in range(len(b) - 1):
            r[i + 1] = r[i] * 10 % m    
        s = 0
        for i in range(len(b)):
            s += b[i] * r[i] 
        if s % m == 0:
            return m 
       
    return 0

#rho- метод Полларда:

def rho_pollard(n, x_0, f):
    X_val = {}
    X = [x_0]
    Y = [x_0]
    X_val[X[0]] = 1

    i = 0
    while X_val[X[i]] != 2:
        X.append(f(X[i], n))
        Y.append(f(f(Y[i], n), n))

        if X[i + 1] not in X_val:
            X_val[X[i + 1]] = 1
        else:
            X_val[X[i + 1]] = X_val[X[i + 1]] + 1

        d = math.gcd(Y[i + 1] - X[i + 1], n)

        if X[i + 1] == Y[i + 1]:
            return 0
        if d != 1:
            return d
        
        i = i + 1
    
    print("Try another x0")
    return 0

#Допоміжні функції для CFRAC:

def legendre(a, p): #символ Лежандра
    i = 1
    while True:
        while a >= p:
            a = a % p
        if a == 1 or a == 0:
            return a * i
        while a % 2 == 0:
            a = a // 2
            if p % 8 == 3 or p % 8 == 5:
                i = -i
        if a % 4 == 3 and p % 4 == 3:
            i = -i
        if a == 1:
            return a * i
        a, p = p, a

def factor_base_creating(n): #створення фактор-бази для конкретного n
    factor_base = []
    for p in prime:
        if legendre(n, p) == 1:
            factor_base.append(p)
    return factor_base

def factor_probni_dilenya(n, factor_base, canonical): #канонічний розклад числа
    canon = canonical.copy()
    
    n_string = str(n)
    b = []
    for i in n_string[::-1]:
        b.append(int(i))

    for m in factor_base:
        r = [0] * len(b)
        r[0] = 1
        for i in range(len(b) - 1):
            r[i + 1] = r[i] * 10 % m    
        s = 0
        for i in range(len(b)):
            s += b[i] * r[i] 
        if s % m == 0:
            canon[factor_base.index(m)] = canon[factor_base.index(m)] + 1
            return factor_probni_dilenya(n // m, factor_base, canon)
    if n == 1:
        return canonical
    return 0

def check_system(S, sample, factor_base):
    null = [0] * len(factor_base)
    sum = null.copy()
    
    for i in sample:
        for k in range(len(factor_base)):
            sum[k] = sum[k] + S[i][2][k]

    for j in range(len(sum)):
        sum[j] = sum[j] % 2

    if sum == null:
        return 1
    return 0

#Метод Брілхарта-Моріссона(CFRAC):

def cfrac(n):

    factor_base = factor_base_creating(n)

    S = {}
    m = int(math.sqrt(n))
    a = [m]
    u = [m]
    v = [1]
    b = [1, a[0]]

    r = []
    i = 0
    while len(r) <= len(factor_base) + 1:
        v.append((n - u[i] ** 2) // v[i])
        a.append(((m + u[i]) // v[i + 1]) // 1)
        u.append(a[i + 1] * v[i + 1] - u[i])
        b.append((b[i + 1] * a[i + 1] + b[i]) % n )
        S[i] = (a[i], b[i + 1], factor_probni_dilenya((b[i + 1] ** 2) % n, factor_base, [0] * len(factor_base)))
        if S[i][2] != 0:
            r.append(i)
        i = i + 1
       
    S_true = dict((k, S[k]) for k in r)  
    k = len(S_true)
    keys = S_true.keys()

    for p in range(0, 500 * k):        
        i = random.sample(keys, random.randint(1, len(keys)))
        if check_system(S_true, i, factor_base) == 1:
            X = 1
            Y = 1
            sum = [0] * len(factor_base)

            if type(i) == list: 
                for j in i:
                    for k in range(len(factor_base)):
                        sum[k] = sum[k] + S[j][2][k]
                    X = X * S_true[j][1]
                X = X % n
                for k in range(len(factor_base)):
                    Y = Y * factor_base[k] ** (sum[k]//2)
            else:
                X = (X * S_true[i][1]) % n
                for k in range(len(factor_base)):  
                    Y = Y * factor_base[k] ** S_true[i][2][k]//2

            if X != Y and X != n - Y:
                r1 = math.gcd(X + Y, n)
                r2 = math.gcd(X - Y, n)
                if r1 == 1 or r2 == 1:
                    continue
                return r1
    print(f"Can`t factor {n}.. :(")
    return 0

#---------------------------------------------------------------------------

def f(x, n):
    return (x ** 2 + 1) % n

def canonical_search(n):
    print(f"The number we want to factor {n}\n")
    factors = []

    print("1.Miller-Rabin primarity")

    start_time = time.time()
    if miller_rabin_primality(n, 10) != 1:
        print(f"{miller_rabin_primality(n, 10)}")
    if miller_rabin_primality(n, 10) == 1:
        end_time = time.time()
        print(f"The number {n} is prime. ")
        elapsed_time = end_time - start_time
        print(f"Elapsed time: {elapsed_time}") 
        return [n]
    
    print("\n2.Metod probnih dilen`")

    while True:
        start_time = time.time()
        a = probni_dilenya(n)
        end_time = time.time()
        if a == 0:
            break
        factors.append(a)
        print(f"The divisor {a} found")
        elapsed_time = end_time - start_time
        print(f"Elapsed time: {elapsed_time}") 
        n =  n // a

    if miller_rabin_primality(n, 100) == 1:
        print(f"The number {n} is prime. ")
        return factors

    print("\n3.rho-Pollard method")
    start_time = time.time()
    a = rho_pollard(n, 2, f)
    end_time = time.time()
    if a != 0:
        print(f"The divisor {a} found")
        elapsed_time = end_time - start_time
        print(f"Elapsed time: {elapsed_time}") 
        factors.append(a)
        n = n // a
        if miller_rabin_primality(n, 100) == 1:
            print(f"The number {n} is prime. ")
            factors.append(n)
            return factors
        

    print("\n4.CFRAC")  

    while True:
        start_time = time.time()
        a = cfrac(n)
        end_time = time.time()  
        if a == 0:
            print(f"Can`t factor {n}.. :(")
            return factors
        print(f"The divisor {a} found")
        elapsed_time = end_time - start_time
        print(f"Elapsed time: {elapsed_time} \n") 
        factors.append(a)
        n = n // a
        if miller_rabin_primality(n, 10) == 1:
            factors.append(n)
            return factors
            
    return factors
        

#a = int(input("Input the number you want to factore:"))
print("\n", canonical_search(a))