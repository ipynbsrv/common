from ipynbsrv.contract.services import EncryptionService, IntegrityService
import rsa

'''
Concrete implementation of the encryption and integrity services using RSA.

:link http://stuvel.eu/rsa
'''
class RSA(EncryptionService, IntegrityService):
    '''
    Initializes a new RSA service.

    :param hash_algorithm: The hashing algorithm to use when signing/verifying integrity.
    '''
    def __init__(self, hash_algorithm='SHA-256'):
        self.hash_algorithm = hash_algorithm

    def decrypt(self, text, key):
        return rsa.decrypt(text, key)

    def encrypt(self, text, key):
        return rsa.encrypt(text, key)

    def sign(self, text, key):
        rsa.sign(text, key, self.hash_algorithm)

    def verify(self, text, signature, key):
        return rsa.verify(text, signature, key)
