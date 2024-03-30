from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
import uuid


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            **extra_fields
            )
        user.set_password(password)
        user.save()
        provider = 'django' if not extra_fields.get('provider') else extra_fields.get('provider')
        Provider.objects.create(name=provider, user=user)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is False:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is False:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=31, blank=True)
    last_name = models.CharField(_('last name'), max_length=31, blank=True)
    picture = models.URLField(_('picture'), blank=True)
    username = None
    uid = models.CharField(max_length=255, blank=True, null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()
    
    def __str__(self):
        return self.email
    
    class Meta:
        db_table = 'user'
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ['-date_joined']


class Provider(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='providers')
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'provider'
        verbose_name = _('provider')
        verbose_name_plural = _('providers')
        ordering = ['-created_at']


