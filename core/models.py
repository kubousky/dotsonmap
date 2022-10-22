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
        user.is_superuser = True
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


class TagPrivate(models.Model):
    """TagPrivate to be used for a position/dot"""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='tags_private',                      #    ->   current_user.tags_private.all()
        on_delete=models.CASCADE,
    )
    public = False

    def __str__(self):
        return self.name

class DotPrivate(models.Model):
    """DotPrivate object"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE       
    )
    name = models.CharField(max_length=255)
    public = False
    description = models.TextField(max_length=350, blank=True)
    lon = models.CharField(max_length=20)
    lat = models.CharField(max_length=20)
    rating = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])
    link = models.CharField(max_length=255, blank=True)
    tag = models.ForeignKey('TagPrivate', on_delete=models.PROTECT)
    image = models.ImageField(null=True, upload_to=dot_image_file_path)

    def __str__(self): # !!! lo vamos a cambiar por un imagen de su TagPrivate, cada 'dot' ser un circulo con rio o montaña etc # puede ser?
        return self.name


# class TagPublic(models.Model):
#     """TagPublic to be used for a position/dot"""
#     name = models.CharField(max_length=255)
#     user = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.PROTECT,
#     )
#     public = True

#     def __str__(self):
#         return self.name

# class DotPublic(models.Model):
#     """DotPrivate object"""
#     user = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.PROTECT       
#     )
#     name = models.CharField(max_length=255)
#     public = True
#     description = models.TextField(max_length=350, blank=True)
#     lon = models.CharField(max_length=20)
#     lat = models.CharField(max_length=20)
#     rating = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])
#     link = models.CharField(max_length=255, blank=True)
#     # !!! importante cambiar: max 1 TagPrivate por DotPrivate and do it required
#     tags = models.ManyToManyField('TagPublic')
#     # tag = models.ForeignKey(TagPrivate, on_delete=models.PROTECT)
#     image = models.ImageField(null=True, upload_to=dot_image_file_path)

#     def __str__(self): # !!! lo vamos a cambiar por un imagen de su TagPrivate, cada 'dot' ser un circulo con rio o montaña etc # puede ser?
#         return self.name