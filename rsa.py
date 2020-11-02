from Crypto.Util.number import getPrime
from util import euler_totient, modular_inverse
import math
import random

class RSA():
  """
  A class used as RSA (Rivest-Shamir-Adlemann) cipher

  Parameters
  ----------
  p : int (first secret large prime)
  q : int (second secret large prime)
  n : int (product of p and q, shared publicly)
  e : int (component of public key, a random large number relatively prime to euler(n))
  d : int (modular inverse of e in modulo euler(n))

  Methods
  -------

  """
  def __init__(self):
    self.n = None
    self.p = None
    self.q = None
    self.e = None
    self.d = None

    self.enc_array = []
    self.dec_array = ''

  # KEY GENERATION
  def generate_key(self):
    '''
    Generate key and paramters used in the RSA scheme
    '''
    bit = random.randint(100, 200)
    self.p = getPrime(bit)
    self.q = getPrime(bit)
    self.n = self.p * self.q
    print('p = {}, q = {}'.format(self.p, self.q))
    totient = (self.p - 1) * (self.q - 1)
    while self.e is None:
      check = random.randint(1, totient)
      if math.gcd(check, totient) == 1:
        self.e = check
    self.d = pow(self.e, -1, totient)

  def save_generated_keys(self, pubfilepath : str, privfilepath : str):
    '''
    Save keys to .pub and .priv file 
    '''
    pubfile_payload = 'RSA;{};{}'.format(self.e, self.n)
    privfile_payload = 'RSA;{};{}'.format(self.d, self.n)

    # Write file .pub
    pbfile = open(pubfilepath, 'w')
    pbfile.write(pubfile_payload)
    pbfile.close()

    # Write file .priv
    prfile = open(privfilepath, 'w')
    prfile.write(privfile_payload)
    prfile.close()

  def import_public_key(self, filepath : str):
    pbfile = open(filepath, 'r')
    pubfile_payload = pbfile.read()
    pbfile.close()
    
    args = pubfile_payload.split(';')
    
    if args[0] != 'RSA' or len(args) != 3:
        print('ERROR: Invalid public key file')
        return
    
    self.e = args[1]
    self.n = args[2]

  def import_private_key(self, filepath : str):
    prfile = open(filepath, 'r')
    privfile_payload = prfile.read()
    prfile.close()
    
    args = privfile_payload.split(';')
    
    if args[0] != 'RSA' or len(args) != 3:
        print('ERROR: Invalid public key file')
        return
    
    self.d = args[1]
    self.n = args[2]

  def encrypt(self):
    self.enc_array = []
    num_rep = str(int.from_bytes(self.msg, byteorder='big'))
    i = 0
    j = 1
    while j <= len(num_rep) + 1:
      lead_zero = 0
      num_cur = int(num_rep[i:j])
      for cr in num_rep[i:j]:
        if cr != '0':
          break
        else:
          lead_zero += 1
      if num_cur > self.n - 1 or j > len(num_rep):
        if j <= len(num_rep):
          j -= 1
          num_cur = num_cur // 10
        b = pow(num_cur, self.e, self.n)
        self.enc_array.append((b, lead_zero))
        i = j
        j = i + 1
      else:
        j += 1

  def decrypt(self):
    assert self.d is not None
    self.dec_array = ''
    for b, lz in self.enc_array:
      b_inv = pow(b, self.d, self.n)
      msg = str(b_inv)
      for i in range(lz):
        msg = '0' + msg
      self.dec_array += str(msg)

  def enc_from_file(self, filepath : str):
    filetarget = open(filepath, 'rb')
    self.msg = filetarget.read()
    filetarget.close()

  def enc_write_file(self, filepath : str):
    enc_file = open(filepath, 'wb')
    enc_msg = ''
    for i in range(len(self.enc_array)):
      enc_msg += str(self.enc_array[i][0])
      enc_msg += 'ab'
      enc_msg += str(self.enc_array[i][1])
      if i < len(self.enc_array) - 1:
          enc_msg += 'ff'
    if len(enc_msg) % 2 == 1:
      enc_msg = '0' + enc_msg
    enc_file.write(
      bytes.fromhex(enc_msg.strip())
    )
    enc_file.close()
  
  def dec_from_file(self, filepath : str):
    self.enc_array = []
    enc_file = open(filepath, 'rb')
    num = enc_file.read().hex()
    print("read ciphertext in hex: ", num)
    arr = num.split('ff')
    for cont in arr:
      cont_arr = cont.split('ab')
      b = int(cont_arr[0])
      lz = int(cont_arr[1])
      self.enc_array.append((b, lz))

  def dec_write_file(self, filepath : str):
    dec_file = open(filepath, 'wb')
    dec_file.write(
      int(self.dec_array).to_bytes(math.ceil(math.log(int(self.dec_array), 256)), byteorder='big')
    )
    dec_file.close()

  def parse_msg_to_enc(self):
    for ch in self.msg:
      print("char in ciphertext: ", ch, chr(ch))
    num = self.msg.hex()
    print("msg in hex: ", num)
    arr = num.split('ff')
    for cont in arr:
      cont_arr = cont.split('ab')
      b = int(cont_arr[0])
      lz = int(cont_arr[1])
      self.enc_array.append((b, lz))

  # GETTER
  def get_input(self, msg : bytes):
    self.msg = msg

  def get_public_key(self):
    assert self.e is not None and self.n is not None
    return self.e, self.n

  def get_private_key(self):
    assert self.d is not None and self.n is not None
    return self.d, self.n

  def get_cipher_text(self):
    print("enc_array length: ", len(self.enc_array))
    enc_msg = ''
    for i in range(len(self.enc_array)):
      enc_msg += str(self.enc_array[i][0])
      enc_msg += 'ab'
      enc_msg += str(self.enc_array[i][1])
      if i < len(self.enc_array) - 1:
        enc_msg += 'ff'
    if len(enc_msg) % 2 == 1:
      enc_msg = '0' + enc_msg
    return str(bytes.fromhex(enc_msg.strip()), 'UTF-8', errors='ignore')

  def get_plain_text(self):
    return str(int(self.dec_array).to_bytes(math.ceil(math.log(int(self.dec_array), 256)), byteorder='big'), 'UTF-8', errors='ignore')

  # SETTER
  def set_public_key(self, e : int, n : int):
    self.e = e
    self.n = n

  def set_private_key(self, d : int, n : int):
    self.d = d
    self.n = n

  def print_params(self):
    print('p (prime 1) = {}'.format(self.p))
    print('q (prime 2) = {}'.format(self.q))
    print('e (public key) = {}'.format(self.e))
    print('d (invers of e modulo (p-1)(q-1)) = {}'.format(self.d))
    print('n (pq) = {}'.format(self.n))

if __name__ == '__main__':

  cipher = RSA()
  cipher.generate_key()
  cipher.get_input(b'Hehehe')
  cipher.encrypt()
  cipher.enc_write_file('tes.txt')
  cipher.dec_from_file('tes.txt')
  cipher.decrypt()
  cipher.dec_write_file('res.txt')
  # cipher.print_params()