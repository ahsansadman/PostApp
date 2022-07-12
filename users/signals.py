from django.db.models.signals import post_save
from django.dispatch import receiver, Signal
from django.core.mail import send_mail
from django.template.loader import render_to_string
from .models import User, Profile

post_signup = Signal()

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_signup)
def send_verification_email(sender, instance=None, created=False, **kwargs):

    context = {
        'user': instance,
    }
    send_mail('Verify Your Email by clicking this url', render_to_string('body.txt', context), from_email='', recipient_list=[instance.email], fail_silently=False)
