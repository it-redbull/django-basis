from django.contrib import admin
from .models import Site, Sitecontent, Revisiecontent

@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'email', 'address', 'formatted_date']
    list_display_links = ['name']
    search_fields = ['name']
    list_per_page = 10
    list_filter = ['name']

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

@admin.register(Sitecontent)
class SitecontentAdmin(admin.ModelAdmin):
    list_display = ['name', 'formatted_date']
    list_display_links = ['name']
    search_fields = ['name']
    list_per_page = 10
    list_filter = ['name']

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False


@admin.register(Revisiecontent)
class RevisiecontentAdmin(admin.ModelAdmin):
    list_display = ['name', 'formatted_date']
    list_display_links = ['name']
    search_fields = ['name']
    list_per_page = 10
    list_filter = ['name']

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False    