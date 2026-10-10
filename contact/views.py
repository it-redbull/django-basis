import email
from email.mime import message
from unicodedata import name
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from .models import Contact, Proefrit
from .forms import Contact, ContactForm, ProefritForm
from django.conf import settings
from core.utils import verify_hcaptcha


def contact(request):
    if request.method == 'POST':

        if not verify_hcaptcha(request):
            messages.error(request, "Captcha verificatie mislukt.")
            return redirect(request.META.get('HTTP_REFERER', '/'))
        
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            send_mail(
            f'Nieuwe contact aanvraag: {form.cleaned_data["subject"]}',
            f'Naam: {form.cleaned_data["name"]}\nEmail: {form.cleaned_data["email"]}\n\n{form.cleaned_data["message"]}',
            settings.DEFAULT_FROM_EMAIL,
            ['mohamed.doudellla@gmail.com'],
        )
        send_mail(
            'Bedankt voor het contact opnemen!',
            f'Hallo {form.cleaned_data["name"]},\n\nWe nemen zo snel mogelijk contact met u op.',
            settings.DEFAULT_FROM_EMAIL,
            [       form.cleaned_data["email"]],
        )
        
        return redirect('contact')
    else:
        form = ContactForm()


    return render(request, 'pages/contact.html', {
        'form': form,
        'hcaptcha_sitekey': settings.HCAPTCHA_SITEKEY,
    })