from django.db import models
from django.core.exceptions import ValidationError
from datetime import datetime
import os
from ckeditor.fields import RichTextField 


class Site(models.Model):
    name = models.CharField(max_length=255)
  
    logo = models.ImageField(upload_to='logo/', blank=True, null=True)
    logo_text = models.ImageField(upload_to='logo/', blank=True, null=True)
    favicon = models.ImageField(upload_to='favicon/', blank=True, null=True)

    instagram_link = models.CharField(max_length=255, blank=True, null=True)
    facebook_link = models.CharField(max_length=255, blank=True, null=True)
    twitter_link = models.CharField(max_length=255, blank=True, null=True)
    whatsapp = models.CharField(max_length=99, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)

    contact_description = models.TextField(blank=True, null=True)

    updated_at = models.DateField(default=datetime.now, blank=True, null=True)

    is_maintenance_mode = models.BooleanField(default=False)
    maintenance_message = models.TextField()



    def __str__(self):
        return self.name

    def clean(self):
        existing_count = Site.objects.count()

        if not self.id and existing_count >= 1:
            raise ValidationError('Only one instance of Site is allowed.')

    def save(self, *args, **kwargs):
        self.clean()  # Validate before saving
        super().save(*args, **kwargs)

    
    def formatted_date(self):
        return self.updated_at.strftime('%d-%m-%Y')




class Sitecontent(models.Model):
    name = models.CharField(max_length=255)
    header_title_1 = models.CharField(max_length=255, blank=True, null=True)
    header_image_1 = models.ImageField(upload_to='header/', blank=True, null=True)
    header_subtitle_1 = models.CharField(max_length=255, blank=True, null=True)

    header_title_2 = models.CharField(max_length=255, blank=True, null=True)
    header_image_2 = models.ImageField(upload_to='header/', blank=True, null=True)
    header_subtitle_2 = models.CharField(max_length=255, blank=True, null=True)

    # about page

    about_title = models.CharField(max_length=255, blank=True, null=True)
    about_image = models.ImageField(upload_to='about/', blank=True, null=True)
    about_description = models.TextField(blank=True, null=True)





    updated_at = models.DateField(default=datetime.now, blank=True, null=True)




    def __str__(self):
        return self.name

    def clean(self):
        existing_count = Sitecontent.objects.count()

        if not self.id and existing_count >= 1:
            raise ValidationError('Only one instance of Site is allowed.')

    def save(self, *args, **kwargs):
        self.clean()  # Validate before saving
        super().save(*args, **kwargs)

    
    def formatted_date(self):
        return self.updated_at.strftime('%d-%m-%Y')



