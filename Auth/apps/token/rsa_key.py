from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519


def generate_rsa(file_name=None):
    # Ed25519

    # Public-private key creation
    private_raw_key = ed25519.Ed25519PrivateKey.generate()
    public_raw_key = private_raw_key.public_key()

    private_key = private_raw_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    
    public_key = public_raw_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    if file_name:
        private_key_file = open(f"{file_name}-rsa.pem", "w")
        private_key_file.write(private_key.decode())
        private_key_file.close()

        public_key_file = open(f"{file_name}-rsa.pub", "w")
        public_key_file.write(public_key.decode())
        public_key_file.close()
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


