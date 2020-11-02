
from Crypto.Util.number import getPrime
import random

class DiffieHellman():
  """
  A class used to generate session key using diffie-hellman algorithm

  '''
  Attributes
  ----------
  n: int
  g: int
  x: int
  y: int

  Methods
  -------
  get_session_key()
    retrieve the session key using the parameters n, g, x, y, that is g^xy (mod n)

  generate_parameters()
    generate the value of the parameters

  set_parameters()
    set the value of the parameters

  get_parameters()
    get the value of the parameters
    
  """
  def __init__(self):
    self.n = None
    self.g = None
    self.x = None
    self.y = None

  def generate_parameters(self):
    bit_1 = random.randint(150, 200)
    bit_2 = random.randint(100, 150)
    self.n = getPrime(bit_1)
    self.g = getPrime(bit_2)
    self.x = random.getrandbits(128)
    self.y = random.getrandbits(128)

  def set_parameters(self, n : int, g : int, x : int, y : int):
    self.n = n
    self.g = g
    self.x = x
    self.y = y

  def get_parameters(self):
    return self.n, self.g, self.x, self.y

  def get_session_key(self):
    return pow(self.g, self.x*self.y, self.n)

