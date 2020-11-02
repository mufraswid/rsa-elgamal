from util import euler_totient

e = int(input('insert e: '))
d = int(input('insert d: '))
p = int(input('insert p: '))
q = int(input('insert q: '))
tot = euler_totient((p-1)*(q-1))
print(e*d%tot)