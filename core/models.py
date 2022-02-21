import uuid
import os
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                        PermissionsMixin
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings


def dot_image_file_path(instance, filename):
    """Generate file path for new dot image"""
    ext =filename.split('.')[-1]
    filename = f'{uuid.uuid4}.{ext}'

    return os.path.join('uploads/dot/', filename)


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):

        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db) # as me has been made

        return user

    def create_superuser(self, email, password):

        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True #comes with PermissionsMixin
        user.save(using=self._db) 

        return user

class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username"""
    email = models.EmailField(max_length=255, unique=True)    
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

class Tag(models.Model):
    """Tag to be used for a position/dot"""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    ) # Do not delet Dots if the user is deleted

    def __str__(self):
        return self.name

class Dot(models.Model):
    """Dot object"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE       
    ) # Do not delet Dots if the user is deleted
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=350, blank=True)
    lon = models.CharField(max_length=20)
    lat = models.CharField(max_length=20)
    rating = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])
    link = models.CharField(max_length=255, blank=True)
    # !!! importante cambiar: max 1 Tag por Dot and do it required
    tags = models.ManyToManyField('Tag')
    image = models.ImageField(null=True, upload_to=dot_image_file_path)

    def __str__(self): # !!! lo vamos a cambiar por un imagen de su Tag, cada 'dot' ser un circulo con rio o montaña etc # puede ser?
        return self.name


    