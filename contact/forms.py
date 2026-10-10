from django import forms
from .models import Contact, Proefrit


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'phone', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Your full name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Your email address'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Your phone number'}),
            'subject': forms.TextInput(attrs={'placeholder': 'Subject of your request'}),
            'message': forms.Textarea(attrs={'placeholder': 'Your message here...'}),
        }


class ProefritForm(forms.ModelForm):
    class Meta:
        model = Proefrit
        fields = ['name', 'email', 'phone', 'message', 'bike', 'bike_id']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Your full name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Your email address'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Your phone number'}),
            'message': forms.Textarea(attrs={'placeholder': 'Your message here...'}),
            'bike': forms.TextInput(attrs={'readonly': 'readonly'}),
            'bike_id': forms.HiddenInput(),
        }



