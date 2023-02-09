from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from apps.common.models import BaseModel
from apps.token.rsa_key import generate_rsa


# Global Variables
User = get_user_model()


class RsaKey(BaseModel):
    public = models.BinaryField(verbose_name='Public Key', editable=False, unique=True)
    private = models.BinaryField(verbose_name='Private Key', editable=False, unique=True)
    active = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["public",'private'],
                name="unique_key_pair"
            )
        ]

    def __str__(self) -> str:
        return f"rsa_key-{self.id}"

    def clean(self):
        if self._state.adding == True:
            if self.public or self.private:
                raise ValidationError(_("Can't set value in an autogenerated field"))
            if not self.active:
                raise ValidationError(_("Sorry you don't need to set value"))
            
            olds = RsaKey.objects.filter(active=True)
            [old.save() for old in olds]

        if self.id:
            self.active = False

    def save(self, *args, **kwargs):
        self.full_clean()
        if self._state.adding == True:
            self.private, self.public = generate_rsa()
        return super().save(*args, **kwargs)


class AuthToken(BaseModel):
    user = models.ForeignKey(User, related_name="auth_token", on_delete=models.CASCADE, null=True, blank=True, editable=False)
    access_token = models.BinaryField(verbose_name='Access Token', editable=False, unique=True, null=True, blank=True)
    exp = models.DateTimeField(default=(timezone.now()+timezone.timedelta(hours=24)), editable=False)
    is_valid = models.BooleanField(default=False, null=True, blank=True)
    payload = models.JSONField(null=True, blank=True, editable=False)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user",'access_token'],
                name="unique_auth_token"
            )
        ]

