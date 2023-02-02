import requests
from datetime import timedelta
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save

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
        if instance.user:
            previous_otps = OTPtoken.objects.filter(user=instance.user).exclude(token=instance.token)
            if previous_otps:
                previous_otps.delete()

        # sending token to user
        if not instance.type == 'Others' and instance.user and instance.token:
            api_key = '60Lj245sqWH0E1BZzN9H1Vod74z35KKw71Vj2ssa'
            url = "https://api.sms.net.bd/sendsms"
            msg = f"Your Care-Box OTP Code is {instance.token}"
            to = str(instance.user.phone).replace('+', '')
            payload = {
                'api_key': api_key,
                'msg': msg,
                'to': to
            }

            response = requests.request("POST", url, data=payload)
            if response.status_code == 200:
                print(response.json())
                # return response.json().get("bkashURL"), response.json().get("paymentID")

@receiver(pre_save, sender=User)
def updateAmbulanceOrder_signal(sender, **kwargs):
    instance = kwargs['instance']

    if instance.id:
       pass

