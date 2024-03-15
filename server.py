import socket
import subprocess
import struct

subprocess.call(['pip', 'install', 'rsa'])
subprocess.call(['pip', 'install', 'cryptography'])
print("hello world server")

#import rsa


SERVER_IP = '127.0.0.1'
SERVER_PORT = 5678

#from rsa.key import newkeys
#(public_key, private_key )= newkeys(2048)
# Print the generated keys
#print( public_key)
#print( private_key)
#n = private_key.n
#d = private_key.d

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
# Generate the RSA private key
key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)

public_key = key.public_key()


public_key_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    
from cryptography.hazmat.primitives import serialization

def private_key_to_bytes(private_key):
    return private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )


pkb =private_key_to_bytes(key)

with open('keyPair.key', 'wb') as f:
        f.write(public_key_pem)
        f.write(b'\n')
        f.write(pkb)



#def decrypt(ciphertext, priv_key):
#   cipher = PKCS1_OAEP.new(priv_key)
#   return cipher.decrypt(ciphertext)
  
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

with socket.socket(socket.AF_INET , socket.SOCK_STREAM) as s:
    s.bind((SERVER_IP, SERVER_PORT))
    print('Server is listening')
    s.listen(1)
    conn,addr = s.accept()
    print(f'Connection accepted from :{addr}')
    with conn:
        while(True):
            val =  conn.recv(1024)
            print(val)
            
            if val.decode('utf-8') == 'y':
                conn.send(public_key_pem)
            else:
                break
             
            encryRandomKey =  conn.recv(1024)
            print(encryRandomKey)
            print(type(encryRandomKey))
            print(type(key))
          
            #rk= decrypt(encryRandomKey, key)
           # cipher = PKCS1_OAEP.new(key)            
           # decrypted = cipher.decrypt(encryRandomKey)
           # rk=decrypted.decode("utf-8")
           
            rk = key.decrypt(
                encryRandomKey,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA1()),
                    algorithm=hashes.SHA1(),
                    label=None
                )
            )
            
            val2 =  conn.recv(1024)
            if val2.decode('utf-8') == 'password':
                conn.send(rk)
            else:
                break
           
         
            break
            

