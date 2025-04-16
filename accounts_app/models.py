# accounts_app/models.py
from django.conf import settings
from django.core.files.storage import default_storage
from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image, UnidentifiedImageError

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('org', 'Organization Representative'),
        ('evaluator', 'Evaluator'),
        ('applicant', 'Applicant'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='applicant')
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    groups = models.ManyToManyField(
        'auth.Group',
        blank=True,
        related_name='customuser_set',
        help_text='The groups this user belongs to.',
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        blank=True,
        related_name='customuser_permissions',
        help_text='Specific permissions for this user.',
    )

    def __str__(self):
        return self.username

    def get_profile_picture_url(self):
        if self.profile_picture and self.profile_picture.storage.exists(self.profile_picture.name):
            return self.profile_picture.url
        return f"{settings.MEDIA_URL}profile_pics/default.png"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.profile_picture and self.profile_picture.storage.exists(self.profile_picture.name):
            try:
                img_path = self.profile_picture.path
                with Image.open(img_path) as img:
                    if img.height > 300 or img.width > 300:
                        img.thumbnail((300, 300))
                        img.save(img_path)
            except FileNotFoundError:
                print(f"Profile picture file not found: {self.profile_picture.name}")
            except UnidentifiedImageError:
                print(f"Invalid image file: {self.profile_picture.name}")
            except OSError as e:
                print(f"OS error while processing profile picture: {e}")


class MyModel(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.name