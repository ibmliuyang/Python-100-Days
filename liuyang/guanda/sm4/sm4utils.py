from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.ciphers import CipherContext
from cryptography.hazmat.primitives.padding import PKCS7
from cryptography.hazmat.backends import default_backend
import base64
import binascii

class SM4Util:
    def __init__(self, key):
        self.key = bytes.fromhex(key)
        self.backend = default_backend()

    def encrypt_ecb(self, plaintext):
        cipher = Cipher(algorithms.SM4(self.key), modes.ECB(), backend=self.backend)
        encryptor = cipher.encryptor()
        padder = PKCS7(algorithms.SM4.block_size).padder()
        padded_data = padder.update(plaintext.encode('utf-8')) + padder.finalize()
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()
        return base64.b64encode(ciphertext).decode('utf-8')

    def decrypt_ecb(self, ciphertext):
        cipher = Cipher(algorithms.SM4(self.key), modes.ECB(), backend=self.backend)
        decryptor = cipher.decryptor()
        decoded_ciphertext = base64.b64decode(ciphertext)
        decrypted_data = decryptor.update(decoded_ciphertext) + decryptor.finalize()
        unpadder = PKCS7(algorithms.SM4.block_size).unpadder()
        unpadded_data = unpadder.update(decrypted_data) + unpadder.finalize()
        return unpadded_data.decode('utf-8')

# 测试
if __name__ == "__main__":
    hex_key = "6707af3a3a7bc393ad4a547a5694c85f"  # 16进制密钥，与Java中的hexKey相对应
    sm4 = SM4Util(hex_key)

    plaintext = '{"nsrsbh":"914400007578948436"}'
    encrypted_text = sm4.encrypt_ecb(plaintext)
    decrypted_text = sm4.decrypt_ecb(encrypted_text)


    decrypted_text = sm4.decrypt_ecb(encrypted_text)
  #  print("Original Text:", plaintext)
   # print("Encrypted Text:", encrypted_text)
    print("Decrypted Text:", decrypted_text)
