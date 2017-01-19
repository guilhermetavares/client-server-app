import codecs
from Crypto.Cipher import AES
from Crypto import Random

KEY123 = '32longbytesforemp786cuskey123cpt'

def encrypt(raw, key=KEY123):
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_CFB, iv)
    msg = iv + cipher.encrypt(raw)
    return codecs.encode(msg, 'hex_codec')


def decrypt(recv, key=KEY123):
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_CFB, iv)
    return cipher.decrypt(codecs.decode(recv, 'hex_codec'))[len(iv):]
