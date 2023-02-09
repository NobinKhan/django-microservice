import json
import pyseto
from pyseto import Key
from django.utils import timezone
from apps.token.models import RsaKey

# secret keys
rsa = RsaKey.objects.filter(active=True)[0]

pem_private_key = rsa.private.tobytes()
pem_public_key = rsa.public.tobytes()

payload = {
    'pyseto': {
        'id': 15,
        'is_active': False,
    },
    'token':{
        'exp': str(timezone.now()),
    }

}

# generate secret key
secret_key = Key.new(version=4, purpose="public", key=pem_private_key)


# get access token with payload
access_token = pyseto.encode(secret_key, payload=payload)

# client server
# generate public key
public_key = Key.new(version=4, purpose="public", key=pem_public_key)
decoded = pyseto.decode(secret_key, access_token)

# check
print(f"\npaseto_secret_key = {secret_key}\n")
print(f"aceess_token = {access_token}\n")
print(f"public_key = {public_key}\n")
print(f"decode = {decoded}\n")
print(f"decoded.payload = {decoded.payload}\n")
print(f"payload = {payload}\n")
con = decoded.payload.decode('utf-8')
print(f"string = {con}\n")
print(f"dict = {json.loads(con)}\n")
print(f"type = {type(con)}\n")