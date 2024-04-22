from django.db import models
from user.models import User
from django_tenants.models import DomainMixin, TenantMixin
# Create your models here.

class Shop(TenantMixin):
    slug = models.SlugField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='shops')
    logo = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    managers = models.ManyToManyField(User, related_name='managed_shops', blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    #default true, the schema will be automatically created and synced when it is saved
    auto_create_schema = True
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if self.id:
            if self.owner is None:
                self.is_active = False
            else:
                self.is_active = True
        else:
            self.is_active = True
        super(Shop, self).save(*args, **kwargs)


class Domain(DomainMixin):
    pass


