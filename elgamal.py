# Elgamal
import random
import math

class Elgamal():
    def __init__(self, prime : int):
        self.prime = prime
        self.msg = None
        self.g = None
        self.x = None
        self.y = None

        self.enc_array = []
        self.dec_array = ''

    # KEY GENERATION
    def generate_key(self):
        self.g = random.randint(1, self.prime - 1)
        self.x = random.randint(1, self.prime - 2)
        self.y = pow(self.g, self.x, self.prime)
    
    def get_public_key(self):
        assert self.g is not None and self.y is not None
        return self.g, self.y, self.prime
    
    def get_private_key(self):
        assert self.x is not None
        return self.x, self.prime
    
    def save_generated_keys(self, pubfilepath : str, privfilepath : str):
        '''
        Save keys to .pub and .priv file 
        '''
        pubfile_payload = 'ELGAMAL;{};{};{}'.format(self.g, self.y, self.prime)
        privfile_payload = 'ELGAMAL;{};{}'.format(self.x, self.prime)

        # Write file .pub
        pbfile = open(pubfilepath, 'w')
        pbfile.write(pubfile_payload )
        pbfile.close()

        # Write file .priv
        prfile = open(privfilepath, 'w')
        prfile.write(privfile_payload)
        prfile.close()

    # IMPORT KEY FROM EXTERNAL SOURCES
    def import_public_key(self, filepath : str):
        pbfile = open(filepath, 'r')
        pubfile_payload = pbfile.read()
        pbfile.close()
        
        args = pubfile_payload.split(';')
        
        if args[0] != 'ELGAMAL' or len(args) != 4:
            print('ERROR: Invalid public key file')
            return
        
        self.g = args[1]
        self.y = args[2]
        self.prime = args[3]
    
    def import_private_key(self, filepath : str):
        prfile = open(filepath, 'r')
        privfile_payload = prfile.read()
        prfile.close()
        
        args = privfile_payload.split(';')
        
        if args[0] != 'ELGAMAL' or len(args) != 3:
            print('ERROR: Invalid public key file')
            return
        
        self.x = args[1]
        self.prime = args[2]

    # ENC AND DEC
    def encrypt(self):
        self.enc_array = []
        num_rep = str(int.from_bytes(self.msg, byteorder='big'))
        i = 0
        j = 1
        k = random.randint(1, self.prime - 2)
        while j <= len(num_rep) + 1:
            lead_zero = 0
            num_cur = int(num_rep[i:j])
            for cr in num_rep[i:j]:
                if cr != '0':
                    break
                else:
                    lead_zero += 1
            if num_cur > self.prime - 1 or j > len(num_rep):
                if j <= len(num_rep):
                    j -= 1
                    num_cur = num_cur // 10
                a = pow(self.g, k, self.prime)
                b = (pow(self.y, k) * (num_cur)) % self.prime
                self.enc_array.append((a, b, lead_zero))
                i = j
                j = i + 1
            else:
                j += 1

    def decrypt(self):
        self.dec_array = ''
        for a, b, lz in self.enc_array:
            a_inv = pow(a, self.prime - 1 - self.x, self.prime)
            msg = (b * a_inv) % self.prime
            msg = str(msg)
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
            enc_msg += 'ab'
            enc_msg += str(self.enc_array[i][2])
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
        arr = num.split('ff')
        for cont in arr:
            cont_arr = cont.split('ab')
            a = int(cont_arr[0])
            b = int(cont_arr[1])
            lz = int(cont_arr[2])
            self.enc_array.append((a, b, lz))

    def dec_write_file(self, filepath : str):
        dec_file = open(filepath, 'wb')
        dec_file.write(
            int(self.dec_array).to_bytes(math.ceil(math.log(int(self.dec_array), 256)), byteorder='big')
        )
        dec_file.close()


    # Getter
    def get_input(self, msg : bytes):
        self.msg = msg
    
    def parse_msg_to_enc(self):
        num = self.msg.hex()
        arr = num.split('ff')
        for cont in arr:
            cont_arr = cont.split('ab')
            a = int(cont_arr[0])
            b = int(cont_arr[1])
            lz = int(cont_arr[2])
            self.enc_array.append((a, b, lz))
    
    def get_cipher_text(self):
        enc_msg = ''
        for i in range(len(self.enc_array)):
            enc_msg += str(self.enc_array[i][0])
            enc_msg += 'ab'
            enc_msg += str(self.enc_array[i][1])
            enc_msg += 'ab'
            enc_msg += str(self.enc_array[i][2])
            if i < len(self.enc_array) - 1:
                enc_msg += 'ff'
        if len(enc_msg) % 2 == 1:
            enc_msg = '0' + enc_msg
        return str(bytes.fromhex(enc_msg.strip()), 'UTF-8', errors='ignore')
    
    def get_plain_text(self):
        return str(int(self.dec_array).to_bytes(math.ceil(math.log(int(self.dec_array), 256)), byteorder='big'), 'UTF-8', errors='ignore')
    

    # Setter
    def set_public_key(self, p : int, g : int, y : int):
        self.prime = p
        self.g = g
        self.y = y

    def set_private_key(self, p : int, x : int):
        self.prime = p
        self.x = x

if __name__ == '__main__':
    print("Hello, World!")
    a = Elgamal(1103)
    a.generate_key()
    a.get_input(b'Hehehe')
    a.encrypt()
    a.enc_write_file('hue.txt')
    a.dec_from_file('hue.txt')
    a.decrypt()
    a.dec_write_file('dec.txt')