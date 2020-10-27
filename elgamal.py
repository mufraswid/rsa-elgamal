# Elgamal
import random

class Elgamal():
    def __init__(self, prime : int):
        self.prime = prime
        self.msg = None
        self.g = None
        self.x = None
        self.y = None

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
        pbfile.write(pubfile_payload)
        pbfile.close()

        # Write file .priv
        prfile = open(privfilepath, 'w')
        prfile.write(privfile_payload)
        prfile.close()

    # IMPORT KEY FROM EXTERNAL SOURCES
    def import_public_key(filepath : str):
        pbfile = open(filepath, 'r')
        pubfile_payload = pbfile.read()
        pbfile.close()
        
        args = pubfile_payload.split(';')
        
        if args[0] != 'ELGAMAL':
            print('ERROR: Invalid public key file')
            return
        
        self.g = args[1]
        self.y = args[2]
        self.prime = args[3]
    
    def import_private_key(filepath : str):
        prfile = open(filepath, 'r')
        privfile_payload = prfile.read()
        prfile.close()
        
        args = privfile_payload.split(';')
        
        if args[0] != 'ELGAMAL':
            print('ERROR: Invalid public key file')
            return
        
        self.x = args[1]
        self.prime = args[2]

