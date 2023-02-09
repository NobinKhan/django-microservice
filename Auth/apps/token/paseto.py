import pyseto
from pyseto import Key



secret_key_pem = b"-----BEGIN PRIVATE KEY-----\nMC4CAQAwBQYDK2VwBCIEILTL+0PfTOIQcn2VPkpxMwf6Gbt9n4UEFDjZ4RuUKjd0\n-----END PRIVATE KEY-----"
public_key_pem = b"-----BEGIN PUBLIC KEY-----\nMCowBQYDK2VwAyEAHrnbu7wEfAP9cGBOAHHwmH4Wsot1ciXBHwBBXQ4gsaI=\n-----END PUBLIC KEY-----"
secret_key = Key.new(version=4, purpose="public", key=secret_key_pem)
token = pyseto.encode(
    secret_key,
    '{"data": "this is a signed message", "exp": "2022-01-01T00:00:00+00:00"}',
)
token
B'v4.public.eyJkYXRhIjogInRoaXMgaXMgYSBzaWduZWQgbWVzc2FnZSIsICJleHAiOiAiMjAyMi0wMS0wMVQwMDowMDowMCswMDowMCJ9l1YiKei2FESvHBSGPkn70eFO1hv3tXH0jph1IfZyEfgm3t1DjkYqD5r4aHWZm1eZs_3_bZ9pBQlZGp0DPSdzDg'
public_key = Key.new(4, "public", public_key_pem)
decoded = pyseto.decode(public_key, token)
decoded.payload
B'{"data": "this is a signed message", "exp": "2022-01-01T00:00:00+00:00"}'