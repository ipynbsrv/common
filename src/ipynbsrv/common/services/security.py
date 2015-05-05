from ipynbsrv.contract.services import EncryptionService, IntegrityService
import rsa


class RSA(EncryptionService, IntegrityService):
    '''
    Concrete implementation of the encryption and integrity services using RSA.

    :link http://stuvel.eu/rsa
    '''

    '''
    Initializes a new RSA service.

    :param hash_algorithm: The hashing algorithm to use when signing/verifying integrity.
    '''
    def __init__(self, hash_algorithm='SHA-256'):
        self.hash_algorithm = hash_algorithm

    def decrypt(self, text, key, **kwargs):
        return rsa.decrypt(text, key)

    def encrypt(self, text, key, **kwargs):
        return rsa.encrypt(text, key)

    def sign(self, text, key, **kwargs):
        hash_algorithm = self.hash_algorithm
        if kwargs.get('hash_algorithm'):
            hash_algorithm = kwargs.get('hash_algorithm')
        return rsa.sign(text, key, hash_algorithm)

    def verify(self, text, signature, key, **kwargs):
        return rsa.verify(text, signature, key)
