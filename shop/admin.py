from django.contrib import admin
from .models import Shop
# Register your models here.


class ShopAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'created_at', 'updated_at')
    search_fields = ('name', 'owner')
    list_filter = ('created_at', 'updated_at')

    def save_model(self, request, obj, form, change):
        # Logic to handle changes made by admins
        if 'is_active' in form.changed_data and not request.user.is_superuser:
            # If is_active field has been changed by a non-superuser, revert it
            obj.is_active = not obj.is_active  # Toggle the value
        super().save_model(request, obj, form, change)


admin.site.register(Shop, ShopAdmin)