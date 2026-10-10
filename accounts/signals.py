from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.template.loader import render_to_string

from .models import CustomUser



@receiver(pre_save, sender=CustomUser)
def send_approval_email(sender, instance, **kwargs):
    if not instance.pk:
        return  # nieuw object, skip

    try:
        old = CustomUser.objects.get(pk=instance.pk)
    except CustomUser.DoesNotExist:
        return

    # Check of is_approved van False naar True gaat
    if not old.is_approved and instance.is_approved:
        subject = 'Votre compte a été validé ! ✅'
        message = render_to_string('accounts/emails/approved.html', {
            'user': instance,
        })
        send_mail(
            subject,
            '',
            settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL')
                else 'noreply@halalhoek.nl',
            [instance.email],
            html_message=message,
            fail_silently=True,
        )
