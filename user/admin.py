from django.contrib import admin
from .models import User, Provider
# Register your models here.

class ProviderInline(admin.TabularInline):
    model = Provider
    extra = 0


class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'picture', 'providers')
    search_fields = ('email', 'first_name', 'last_name')
    readonly_fields = ('id', 'date_joined', 'last_login')
    ordering = ('-date_joined',)

    def providers(self, obj):
        return ', '.join([provider.name for provider in obj.providers.all()])


admin.site.register(User, UserAdmin)
