import json
import pyseto
from pyseto import Key
from django.utils import timezone

# secret keys
pem_private_key = b"-----BEGIN PRIVATE KEY-----\nMIIFLTBXBgkqhkiG9w0BBQ0wSjApBgkqhkiG9w0BBQwwHAQIBu4PTflo9fwCAggAMAwGCCqGSIb3DQIJBQAwHQYJYIZIAWUDBAEqBBDG888wIFirPva6p4P4RWsCBIIE0Kr6DqOLQqJHK+1MvQr83DE+mypYsFoRcQK6OXPK7amCB4lEWvZrQiuARVYfmwaL/uc8z4SxS/TuIZkjVGMuewXd/LmAx5RbynO7hsd+3IEaDkUvjQCudZ4jtAVViVbNkJ0lTMwSMBx2bNXMTVrY4u4whtQLgzSBZTBrXUhBbe5zrX465Mv1EKQXtF6WDhMjE7Y48YmTjD/WX0tc/3N5tqZUHAu5VoHdSCHYQK1GWCOuF+9g93vSgcoyAKJea8jK2etKV91Qd9Gbj7xfhGS274ExuuyNNyVi4o/LjroaQN41/6F54TbbI34znZRu7kmj3lCad9QHs8bi3C4sw7PgyZEFfVZ92/rQxOD/AUw8ftrm9jHyeBh0NDmOp4EPTUYiYJNMRDwwTpFeE9fLrS0a4swC8B4C48MgE05ZAgLgQyqXLoAvutgEIbTsTWpZ1LtG1bot29b6QewOWUdV1CKygpNjjEx+smdFEt47L4+2rYlU/VTreoP2Djkcq6UUKLVXr7ZVXwkcXWdkKpjCMWQIDbHIzlLrlnWWp1zMSJ0GH9bESSZJOtYE+8q6szj/sWkcz8I8GRih9/bd6pG4hlyOVeHvmEx2kqhxSDrkAQ7ge/s2QzzutkWwnjBHge/jwyH71fMndCIq+I/TvxsDWj1a9mYr3g6mA2JCg+ctegQbqwV537BXHbWER8bHaAL2My1+1YR9dwEVsL/8uChoZ50KMje67YwvUMFKJENjQy8HoZ8yqf6xXvbgIeRTD+PR+Oed5/hk4cadOSzK6lSw7ZEru+RNwi3ohlUyijci+jQRTW6yHqQMkkr+Fs0YC6sVIJj34MovtmONZtLi/RI7G2Zd/4eKJBmnCYKvDZGltKOXzXfQV4oRWmHXQgm2d/MiDu7u4Txoz8lPJatjj0ADkZJ69sLTKJcnZFT8wD9o24lN5G+8SFZeWOfNfKrbkbdfINKN2x3lV7G0P6Wz7tG3u14Pu5orUqsgEGgqpuCoWxSQ0bhjBm26n/8rIEuPVmM00kXdE5XZMRrktg4gSNlgck9Bbeje+8FU5TsGnLzIKi6guP7FIIHybCEZEoYXBvgW4BcafeuxiGRM/PlWHtx8aTVB0sSQEJWyEZHRSgifD68Ny5+gvA84qPx0mXucm56kSjK1JAn0Zcy6X5a7s6Dfs9aqXd9XBL6Ctk2L3zt1cAVoGclVPgkECNclfkVa0E7kibGJxyjD8GcM+CjbL7mQPFNUK56hiDp+BHskp4qhj7vqObnMkNMLfs4Xl2ufCUCObwPKNEQHdT5NuTSKSECBg+lIC8UQGi8Go9j+4uGMCNnQn3a0XVKC8MVqpgCrWWNO57576Cq5DaLnftkftVXqjAMVtsOxkb4kUoH84BSoMiSrxbeO6UD9p+7UPOXEl5Zz7iJSU+QqnlW45g6L0qSsRlvnp8iDPS7qRKnAis4QiXyVtL0/GXhc6j9dtccAdHbDpCyoopZ2Qy4kzlZkxBU4bBj4i/Sz8A9R0W7T0OUmwGZ/FKkeHH/cyu7vJlikZtEiZQYWCo5AbFQfxqx/FEZjtrr/Mir4ErUK8bE/jVR6yYkVd8QfsWi8Ggj8D2v6c03ltBK1hAuaQrOY6u72Z7PhIfMZl1eAOQB6keOcaRYDuUPrWpvd\n-----END PRIVATE KEY-----"
pem_public_key = b"-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAqir0uoWmkNNfMbGufQcpyCrcBeb5l2Lk7U5P6H4HOj5qMwahFEtHyd9pqD88rHrScv7ctIrllz3IgVvXElv7qpW4t+JRxNPaS4vywrr0aYZVOxJOqCPAO+iRor8AN1BIfK7bl9QuJIiBF6AMeY5r/or7hRpCkr7a5GyxehqdvjouMBiyMb2cxliksCzmzvuPAQREeBLDGR9So/RCSzLiO8vKL+HRdk+LjGPegQ1SeB4mYDQzVxGtJ7rkTXDiwYcToPcoRvh2IZj/D252IDMggDqHkAPql0xWWjO3UQCA2frGzMGCnf8crNSS8TcvATwwWwrzLR1Dn8ESg/vKwi985QIDAQAB\n-----END PUBLIC KEY-----"

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