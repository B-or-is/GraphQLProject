from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

# from .models import Model, Make, Car
from .models import Model, Make, Car, ApiClient

admin.site.register(Make)
admin.site.register(Model)
admin.site.register(Car)


class ApiClientAdmin(UserAdmin):
    models = ApiClient
    ordering = ['email']
    list_display = (
        'email', 'first_name', 'last_name', 'is_staff', 'is_superuser')
    search_fields = ('first_name', 'last_name', 'email')  # 🖘 no username
    fieldsets = (
        (None, {'fields': ('password',)}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser',),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
            #              🖞 without username
        }),
    )


admin.site.register(ApiClient, ApiClientAdmin)
