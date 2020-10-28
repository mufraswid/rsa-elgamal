p = 2357
g = 2
x = 1751
y = pow(g, x, p)
m = 2035
k = 8


print(p, g, x, y)
a = pow(g, k, p)
b = (pow(y, k) * m) % p
print(a, b)

a_inv = pow(a, p - 1 - x, p)
ms = (a_inv * b) % p
print(a_inv, ms)