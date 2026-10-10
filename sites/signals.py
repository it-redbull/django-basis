from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.conf import settings

from .models import Site, Sitecontent, Revisiecontent

@receiver(post_migrate)
def create_initial_records(sender, **kwargs):
    # Create initial Site record
    if Site.objects.count() == 0:
        Site.objects.create(
            name='SiteTitle',
            sitecontent=Sitecontent.objects.first(),
            revisiecontent=Revisiecontent.objects.first(),
        )

    # Create initial Sitecontent record
    if Sitecontent.objects.count() == 0:
        Sitecontent.objects.create(
            name='SiteContent',
        )

    if Revisiecontent.objects.count() == 0:
        Revisiecontent.objects.create(
            name='RevisieContent',
        )

    
