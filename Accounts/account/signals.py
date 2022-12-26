from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import User, OTPtoken



@receiver(post_save, sender=User)
def user_post_Signal(sender, **kwargs):

    instance = kwargs['instance']

    if kwargs.get('created'):
        if not instance.is_active:
            previous_otp = OTPtoken.objects.filter(type='Register', user=instance)
            if previous_otp:
                previous_otp.delete()
            otp = OTPtoken(type='Register', user=instance)
            otp.save()



@receiver(pre_save, sender=User)
def updateAmbulanceOrder_signal(sender, **kwargs):
    instance = kwargs['instance']

    if instance.id:
       pass