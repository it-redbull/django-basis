from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    """Manager voor CustomUser: login via e-mail in plaats van username."""

    def create_user(self, email, first_name, last_name, password=None, **extra_fields):
        if not email:
            raise ValueError('E-mailadres is verplicht')

        email = self.normalize_email(email)

        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            **extra_fields,
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, first_name, last_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_approved', True)
        extra_fields.setdefault('account_type', 'employee')

        return self.create_user(
            email,
            first_name,
            last_name,
            password,
            **extra_fields,
        )


class CustomUser(AbstractBaseUser, PermissionsMixin):

    ACCOUNT_TYPES = [
        ('customer', 'Customer'),
        ('employee', 'Employee'),
        ('partner', 'Partner'),
    ]

    email = models.EmailField(
        'E-mailadres',
        unique=True
    )

    first_name = models.CharField(
        'Voornaam',
        max_length=50
    )

    last_name = models.CharField(
        'Achternaam',
        max_length=50
    )

    phone = models.CharField(
        'Telefoonnummer',
        max_length=20,
        blank=True
    )

    account_type = models.CharField(
        'Accounttype',
        max_length=20,
        choices=ACCOUNT_TYPES,
        default='customer',
    )

    is_approved = models.BooleanField(
        'Goedgekeurd',
        default=False,
        help_text='Bepaalt of deze gebruiker toegang heeft.'
    )

    approved_at = models.DateTimeField(
        'Goedgekeurd op',
        null=True,
        blank=True
    )

    approved_by = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_users',
        verbose_name='Goedgekeurd door',
    )

    is_active = models.BooleanField(
        'Actief',
        default=True
    )

    is_staff = models.BooleanField(
        'Staflidmaatschap',
        default=False
    )

    is_beta_tester = models.BooleanField(
        'Beta Tester',
        default=False
    )

    date_joined = models.DateTimeField(
        'Aangemeld op',
        default=timezone.now
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = 'Gebruiker'
        verbose_name_plural = 'Gebruikers'
        ordering = ['-date_joined']

    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.email})'

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def is_partner(self):
        return self.account_type == 'partner'

    @property
    def is_customer(self):
        return self.account_type == 'customer'

    @property
    def is_employee_account(self):
        return self.account_type == 'employee'

    def approve(self, approved_by=None):
        self.is_approved = True
        self.approved_at = timezone.now()
        self.approved_by = approved_by

        self.save(
            update_fields=[
                'is_approved',
                'approved_at',
                'approved_by',
            ]
        )


class PartnerProfile(models.Model):

    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='partner_profile',
        limit_choices_to={'account_type': 'partner'},
    )

    company_name = models.CharField(
        'Bedrijfsnaam',
        max_length=200
    )

    contact_name = models.CharField(
        'Contactpersoon',
        max_length=200,
        blank=True
    )

    phone = models.CharField(
        'Zakelijk telefoonnummer',
        max_length=30,
        blank=True
    )

    address = models.CharField(
        'Adres',
        max_length=255,
        blank=True
    )

    city = models.CharField(
        'Plaats',
        max_length=100,
        blank=True
    )

    country = models.CharField(
        'Land',
        max_length=100,
        default='Morocco'
    )

    notes = models.TextField(
        'Interne notities',
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.company_name