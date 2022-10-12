from importlib.resources import read_binary
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import base64

# 128bits block size
aes_block_size = 16
iv=b'0000000000000000'

def aes_cbc_encrypt(message, key):
    '''
    use AES CBC to encrypt message, using key and init vector
    :param message: the message to encrypt
    :param key: the secret
    :return: bytes init_vector + encrypted_content
    '''
    iv_len = 16
    assert type(message) in (str,bytes)
    assert type(key) in (str,bytes)
    if type(message) == str:
        message = bytes(message, 'utf-8')
    if type(key) == str:
        key = bytes(key, 'utf-8')
    backend = default_backend()
    #iv = bytes('0'*16,'utf-8')
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(message) + padder.finalize()
    enc_content = encryptor.update(padded_data) + encryptor.finalize()
    return iv + enc_content

def aes_cbc_decrypt(content, key):
    '''
    use AES CBC to decrypt message, using key
    :param content: the encrypted content using the above protocol
    :param key: the secret
    :return: decrypted bytes
    '''
    assert type(content) == bytes
    assert type(key) in (bytes, str)
    if type(key) == str:
        key = bytes(key, 'utf-8')
    # assert len(content) >= 16
    #iv = bytes('0'*16,'utf-8')
    enc_content = content[16:]
    backend = default_backend()
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    unpadder = padding.PKCS7(128).unpadder()
    decryptor = cipher.decryptor()
    dec_content = decryptor.update(enc_content) + decryptor.finalize()
    real_content = unpadder.update(dec_content) + unpadder.finalize()
    return real_content

with open('zImage_old','rb') as file:
#with open('zImage','rb') as file:
	f=file.read()

#with open('key.bin','wb') as kfile:
#	kfile.write(b'MohammedFayaz003')
	
with open('key.key','rb') as kfile:
	k=kfile.read()
	
enc=aes_cbc_encrypt(f,k)

with open('zImage','wb') as e:
#with open('zImage-enc','wb') as e:
	e.write(enc)
'''
dec=aes_cbc_decrypt(enc,k)

with open('UCOS-dec.bin','wb') as d:
#with open('zImage-dec','wb') as d:
	d.write(dec)
#print(enc,'\n',dec)
'''
