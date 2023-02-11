import json
import pyseto
from datetime import timedelta
from typing import Union

from apps.token.models import RsaKey
from django.utils.translation import gettext_lazy as _
from .exceptions import TokenBackendError
from .utils import format_lazy




class TokenBackend:
    def __init__(self,verifying_key="",audience=None,issuer=None,leeway: Union[float, int, timedelta] = None,):
        self.verifying_key = verifying_key
        self.audience = audience
        self.issuer = issuer
        self.leeway = leeway

    def get_leeway(self) -> timedelta:
        if self.leeway is None:
            return timedelta(seconds=0)
        elif isinstance(self.leeway, (int, float)):
            return timedelta(seconds=self.leeway)
        elif isinstance(self.leeway, timedelta):
            return self.leeway
        else:
            raise TokenBackendError(
                format_lazy(
                    _(
                        "Unrecognized type '{}', 'leeway' must be of type int, float or timedelta."
                    ),
                    type(self.leeway),
                )
            )

    def get_verifying_key(self, token):

        return self.verifying_key

    def encode(self, payload: dict):
        """
        Returns an encoded token for the given payload dictionary.
        """
        if not bool(payload):
            return None

        # secret keys
        rsa = RsaKey.objects.filter(active=True)
        if rsa.count() != 1:
            return None
        pem_private_key = rsa.private.tobytes()
        # pem_public_key = rsa.public.tobytes()

        # generate secret key
        secret_key = pyseto.Key.new(version=4, purpose="public", key=pem_private_key)

        # get access token with payload
        jwt_payload = payload.copy()
        if self.audience is not None:
            jwt_payload["aud"] = self.audience
        if self.issuer is not None:
            jwt_payload["iss"] = self.issuer
        access_token = pyseto.encode(secret_key, payload=jwt_payload)

        return access_token

    def decode(self, token, verify=True):
        """
        Performs a validation of the given token and returns its payload
        dictionary.

        Raises a `TokenBackendError` if the token is malformed, if its
        signature check fails, or if its 'exp' claim indicates it has expired.
        """
        # secret keys
        rsa = RsaKey.objects.filter(active=True)[0]
        # pem_private_key = rsa.private.tobytes()
        pem_public_key = rsa.public.tobytes()

        # decode access token
        secret_key = pyseto.Key.new(version=4, purpose="public", key=pem_public_key)
        decode = pyseto.decode(secret_key, token)
        payload = decode.payload.decode('utf-8')

        return json.loads(payload)
        # try:
        #     return jwt.decode(
        #         token,
        #         self.get_verifying_key(token),
        #         algorithms=[self.algorithm],
        #         audience=self.audience,
        #         issuer=self.issuer,
        #         leeway=self.get_leeway(),
        #         options={
        #             "verify_aud": self.audience is not None,
        #             "verify_signature": verify,
        #         },
        #     )
        # except InvalidAlgorithmError as ex:
        #     raise TokenBackendError(_("Invalid algorithm specified")) from ex
        # except InvalidTokenError as ex:
        #     raise TokenBackendError(_("Token is invalid or expired")) from ex
