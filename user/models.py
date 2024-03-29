from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(email=self.normalize_email(email))
        if password:
            user.set_password(password)
        self.save(user, commit=True)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(commit=True)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    firebase_uid = models.CharField(max_length=255, blank=True)  # Optional field for future use

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)

    password = models.CharField(max_length=255)

    objects = UserManager()

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    def __str__(self):
        return self.email
    

class Provider(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.TextField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
