import hashlib
import random
from sympy import isprime, nextprime, primitive_root, gcd

bit_length = random.randint(20, 40)  # Випадкова довжина в бітах

while True:
    p = nextprime(random.getrandbits(bit_length))  # Генеруємо випадкове число
    if isprime(p):  # Перевіряємо, чи є число простим
        break

g = primitive_root(p)

a = random.randint(1, p-1)

b = pow(g, a, p)

while True:
    k = random.randint(1, p-1)  # Генеруємо випадкове число k
    if gcd(k, p-1) == 1:  # Перевіряємо, чи є k і (p-1) взаємно простими
        break

r = pow(g, k, p)

m = input("Введіть повідомлення: ")
H = hashlib.sha256(m.encode()).hexdigest()

def calculate_s(H1, a1, r1, k1, p1):
    p_minus_1 = p1 - 1
    k_inverse = pow(k1, -1, p_minus_1)  # Обернений елемент k модуля (p-1)
    
    s1 = ((int(H1, 16) - a1*r1) * k_inverse) % p_minus_1
    return s1

s = calculate_s(H, a, r, k, p)

while True:
    if gcd(s, p-1) == 1:  # Перевіряємо, чи є s і (p-1) взаємно простими
        break

signature = (r, s)

y = pow(b, -1, p)

p_minus_1 = p - 1
s_inverse = pow(s, -1, p_minus_1)  # Обернений елемент s модуля (p-1)
u1 = (int(H, 16) * s_inverse) % p_minus_1
u2 = (r * s_inverse) % p_minus_1

def calculate_v(g, u1, y, u2, p):
    v = 1
    v = (v * pow(g, u1, p)) % p
    v = (v * pow(y, u2, p)) % p
    return v

v = calculate_v(g, u1, y, u2, p)
if v == r:
    print('рівне')
else:
    print('не то')
