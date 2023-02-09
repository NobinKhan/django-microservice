from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey


# def old_generate_rsa(key=None, file_name=None):
#     rsa_private_key = rsa.generate_private_key(
#         public_exponent=65537,
#         key_size=2048
#     )
    
#     if not key and not SECRET_KEY:
#         key = uuid4()
#     elif SECRET_KEY:
#         key = SECRET_KEY

#     private_key_password = bytes(key, encoding='utf-8')

#     # private key
#     private_key = rsa_private_key.private_bytes(
#         encoding=serialization.Encoding.PEM,
#         format=serialization.PrivateFormat.PKCS8,
#         encryption_algorithm=serialization.BestAvailableEncryption(private_key_password)
#     )

#     # public key
#     public_key = rsa_private_key.public_key().public_bytes(
#     encoding=serialization.Encoding.PEM,
#     format=serialization.PublicFormat.SubjectPublicKeyInfo
#     )

#     if file_name:
#         private_key_file = open(f"./token/rsa/{file_name}-rsa.pem", "w")
#         private_key_file.write(private_key.decode())
#         private_key_file.close()

#         public_key_file = open(f"./token/rsa/{file_name}-rsa.pub", "w")
#         public_key_file.write(public_key.decode())
#         public_key_file.close()
    
#     return private_key, public_key

def generate_rsa(file_name=None):
    # Ed25519

    # Public-private key creation
    private_key = Ed25519PrivateKey.generate()
    public_key = private_key.public_key()
    print(private_key.private_bytes())
    print(type(public_key))
    return private_key, public_key




    '''
    # # Signature creation
    # message = b'Fundamental Cryptography in Python'
    # signature = private_key.sign(message)

    # # Signature verification
    # try:
    #     public_key.verify(signature, message)
    # except InvalidSignature:
    #     # Should not happen
    #     assert False

    # # Wrong message
    # wrong_message = b''
    # try:
    #     public_key.verify(signature, wrong_message)
    # except InvalidSignature:
    #     pass
    # else:
    #     # Should not happen
    #     assert False

    # # Wrong signature
    # wrong_signature = b''
    # try:
    #     public_key.verify(wrong_signature, message)
    # except InvalidSignature:
    #     pass
    # else:
    #     # Should not happen
    #     assert False

    # # Wrong public key
    # wrong_private_key = Ed25519PrivateKey.generate()
    # wrong_public_key = wrong_private_key.public_key()
    # try:
    #     wrong_public_key.verify(signature, message)
    # except InvalidSignature:
    #     pass
    # else:
    #     # Should not happen
    #     assert False
    '''


