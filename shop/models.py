from django.db import models
from user.models import User
# Create your models here.

class Shop(models.Model):
    slug = models.SlugField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='shops')
    logo = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    managers = models.ManyToManyField(User, related_name='managed_shops')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if self.id and self.owner is None:
            self.is_active = False        
        super(Shop, self).save(*args, **kwargs)

