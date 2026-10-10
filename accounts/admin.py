from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils import timezone
from django.contrib import messages

from .models import CustomUser, PartnerProfile


class PartnerProfileInline(admin.StackedInline):
    model = PartnerProfile
    extra = 0
    can_delete = False


@admin.action(description='Geselecteerde partners goedkeuren')
def approve_partners(modeladmin, request, queryset):

    if not request.user.is_superuser:
        modeladmin.message_user(
            request,
            'Alleen een superuser kan partners goedkeuren.',
            level=messages.ERROR
        )
        return

    partners = queryset.filter(
        account_type='partner',
        is_approved=False
    )

    count = 0

    for user in partners:
        user.is_approved = True
        user.approved_at = timezone.now()
        user.approved_by = request.user

        user.save(
            update_fields=[
                'is_approved',
                'approved_at',
                'approved_by',
            ]
        )

        count += 1

    modeladmin.message_user(
        request,
        f'{count} partner(s) goedgekeurd.',
        level=messages.SUCCESS
    )


@admin.action(description='Goedkeuring van partners intrekken')
def revoke_partner_approval(modeladmin, request, queryset):

    if not request.user.is_superuser:
        modeladmin.message_user(
            request,
            'Alleen een superuser kan goedkeuring intrekken.',
            level=messages.ERROR
        )
        return

    partners = queryset.filter(
        account_type='partner',
        is_approved=True
    )

    count = partners.update(
        is_approved=False,
        approved_at=None,
        approved_by=None,
    )

    modeladmin.message_user(
        request,
        f'Goedkeuring van {count} partner(s) ingetrokken.',
        level=messages.SUCCESS
    )


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    list_display = [
        'email',
        'first_name',
        'last_name',
        'account_type',
        'is_approved',
        'is_active',
        'is_staff',
        'date_joined',
    ]

    list_filter = [
        'account_type',
        'is_approved',
        'is_active',
        'is_staff',
        'is_beta_tester',
        'date_joined',
    ]

    search_fields = [
        'email',
        'first_name',
        'last_name',
        'phone',
    ]

    ordering = ['-date_joined']

    actions = [
        approve_partners,
        revoke_partner_approval,
    ]

    fieldsets = (
        (
            None,
            {
                'fields': (
                    'email',
                    'password',
                )
            }
        ),

        (
            'Persoonlijke info',
            {
                'fields': (
                    'first_name',
                    'last_name',
                    'phone',
                )
            }
        ),

        (
            'Account',
            {
                'fields': (
                    'account_type',
                )
            }
        ),

        (
            'Goedkeuring',
            {
                'fields': (
                    'is_approved',
                    'approved_at',
                    'approved_by',
                )
            }
        ),

        (
            'Rechten',
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_beta_tester',
                    'is_superuser',
                    'groups',
                    'user_permissions',
                )
            }
        ),

        (
            'Datums',
            {
                'fields': (
                    'last_login',
                    'date_joined',
                )
            }
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': (
                    'email',
                    'first_name',
                    'last_name',
                    'phone',
                    'account_type',
                    'password1',
                    'password2',
                    'is_approved',
                    'is_active',
                ),
            }
        ),
    )

    readonly_fields = [
        'approved_at',
        'approved_by',
        'date_joined',
        'last_login',
    ]

    def get_inline_instances(self, request, obj=None):
        """
        Toon PartnerProfile alleen wanneer de gebruiker een partner is.
        """
        if obj and obj.account_type == 'partner':
            self.inlines = [PartnerProfileInline]
        else:
            self.inlines = []

        return super().get_inline_instances(request, obj)


@admin.register(PartnerProfile)
class PartnerProfileAdmin(admin.ModelAdmin):

    list_display = [
        'company_name',
        'user',
        'city',
        'country',
        'phone',
        'created_at',
    ]

    search_fields = [
        'company_name',
        'user__email',
        'user__first_name',
        'user__last_name',
        'phone',
    ]

    list_filter = [
        'country',
        'city',
    ]



