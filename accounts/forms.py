from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm

User = get_user_model()


class RegistrationForm(forms.ModelForm):
    """Registratieformulier voor nieuwe gebruikers."""

    password1 = forms.CharField(
        label='Wachtwoord',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Kies een wachtwoord',
        }),
        min_length=8,
        help_text='Minimaal 8 tekens.',
    )
    password2 = forms.CharField(
        label='Wachtwoord bevestigen',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Herhaal je wachtwoord',
        }),
    )
    terms = forms.BooleanField(
        required=True,
        error_messages={'required': 'Ga akkoord met de voorwaarden om verder te gaan.'},
    )

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'phone']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'jouw@email.nl',
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Voornaam',
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Achternaam',
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '06-12345678',
            }),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email', '').lower()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Dit e-mailadres is al in gebruik.')
        return email

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get('password1')
        p2 = cleaned.get('password2')
        if p1 and p2 and p1 != p2:
            self.add_error('password2', 'Wachtwoorden komen niet overeen.')
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class EmailLoginForm(AuthenticationForm):

    username = forms.EmailField(
        label='E-mailadres',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'jouw@email.nl',
            'autofocus': True,
        }),
    )
    password = forms.CharField(
        label='Wachtwoord',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Wachtwoord',
        }),
    )


class CustomPasswordChangeForm(PasswordChangeForm):
    """Wachtwoord wijzigen formulier met styling."""

    old_password = forms.CharField(
        label='Huidig wachtwoord',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Huidig wachtwoord',
            'autocomplete': 'current-password',
        }),
    )
    new_password1 = forms.CharField(
        label='Nieuw wachtwoord',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nieuw wachtwoord',
            'autocomplete': 'new-password',
        }),
    )
    new_password2 = forms.CharField(
        label='Nieuw wachtwoord bevestigen',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Herhaal je nieuwe wachtwoord',
            'autocomplete': 'new-password',
        }),
    )


class ProfileForm(forms.ModelForm):
    """Persoonlijke gegevens aanpassen op de profielpagina."""

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone']
        labels = {
            'first_name': 'Voornaam',
            'last_name': 'Achternaam',
            'email': 'E-mailadres',
            'phone': 'Telefoonnummer',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'given-name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'family-name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'autocomplete': 'email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'tel', 'placeholder': '06 12345678'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email', '').lower()
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('Dit e-mailadres is al in gebruik.')
        return email