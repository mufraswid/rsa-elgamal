

def modular_expo(base, power, mod):
  """
  Returns the value of base raised to the power of power reduced modulo mod

  Parameters
  ----------
  base : int
  power : int
  mod : int 
  """
  ret = 1
  while power > 0:
    if power % 2 == 1:
      ret = ret * base % mod
    base = base * base % mod
    power = int(power / 2)
  return ret

def euler_totient(n : int) -> int:
  """
  Returns the value of euler function of n, which counts the number of positive integers not greater
  than n that is relatively prime to n

  Parameters
  ----------
  n : int
  """
  if n == 1:
    return 1
  ret = n
  temp = 2
  while temp * temp <= n:
    if n % temp == 0:
      ret -= ret // temp
      while n % temp == 0:
        n = n // temp
    temp += 1
  if n > 1:
    ret -= ret // n
  return ret

def extended_gcd(a : int, b : int):
  """
  https://stackoverflow.com/questions/4798654/modular-multiplicative-inverse-function-in-python
  """
  if a == 0:
    return (b, 0, 1)
  else:
    g, y, x = extended_gcd(b % a, a)
    return (g, x - (b // a) * y, y)

def modular_inverse(a : int, mod : int):
  """
  https://stackoverflow.com/questions/4798654/modular-multiplicative-inverse-function-in-python
  """
  g, x, y = extended_gcd(a, mod)
  if g != 1:
    raise Exception('modular inverse does not exist')
  else:
    return x % mod

if __name__ == '__main__':
  # a = 2
  # b = 10
  # print('2^10 mod 1001 is {}'.format(modular_expo(2, 10, 1001)))

  # for i in range(1, 11):
  #   print('euler({}) is {}'.format(i, euler_totient(i)))

  a = 3
  b = 7
  print(modular_inverse(3, 7))