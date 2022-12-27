from datetime import timedelta
from django.utils import timezone
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import User, OTPtoken



@receiver(post_save, sender=User)
def user_post_Signal(sender, **kwargs):

    instance = kwargs['instance']

    if kwargs.get('created'):
        if not instance.is_active and instance.phone:
            previous_otp = OTPtoken.objects.filter(type='Register', user=instance)
            if previous_otp:
                previous_otp.delete()
            otp = OTPtoken(type='Register', user=instance)
            otp.save()


@receiver(post_save, sender=OTPtoken)
def otp_post_Signal(sender, **kwargs):
    instance = kwargs['instance']
    if kwargs.get('created'): # deleting previous objects
        previous_otps = OTPtoken.objects.filter(created__lt=timezone.now() - timedelta(days=2)).exclude(type='Others')
        if previous_otps:
            previous_otps.delete()
        previous_otps = OTPtoken.objects.filter(is_active=False, created__lt=timezone.now() - timedelta(days=2))
        if previous_otps:
            previous_otps.delete()




@receiver(pre_save, sender=User)
def updateAmbulanceOrder_signal(sender, **kwargs):
    instance = kwargs['instance']

    if instance.id:
       pass