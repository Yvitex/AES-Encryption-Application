import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

'''
    Core function of the program
    Use encrypt_aes() to encrypt data
    Use decrypt_aes() to decrypt data
    They IV must be 16 character long
'''

class EncryptionUtility:
    def __init__(self, secret_key, iv):
        if len(secret_key) != 16:
            self.clear_params()
            print("Your Secret Key must be 16 character long")
        elif len(iv) != 16:
            self.clear_params()
            print("Your IV must be 16 character long")
        else:
            self.secret_key = secret_key
            self.iv = iv

    def encrypt_aes(self, data):
        if self.secret_key is None or self.iv is None:
            return "Cannot be encrypted due to wrong secret key or IV"
        else:
            print(len(self.secret_key))
            binary_data = data.encode('utf-8')
            cipher = AES.new(self.secret_key, AES.MODE_CBC, self.iv)
            padded_data = pad(binary_data, AES.block_size)
            ciphertext = cipher.encrypt(padded_data)
            base64_encoded = base64.b64encode(ciphertext)
            return base64_encoded.decode('utf-8')

    def decrypt_aes(self, data):
        if self.secret_key is None or self.iv is None:
            return "Cannot be decrypted due to wrong secret key or IV"
        else:
            actual_ciphertext = base64.b64decode(data)
            iv = self.iv
            cipher = AES.new(self.secret_key, AES.MODE_CBC, iv)
            decrypted_data = cipher.decrypt(actual_ciphertext)
            unpadded_data = unpad(decrypted_data, AES.block_size)
            return unpadded_data.decode('utf-8')

    def clear_params(self):
        self.secret_key = None
        self.iv = None