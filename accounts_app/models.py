# accounts_app/models.py
from django.conf import settings
from django.core.files.storage import default_storage
from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image, UnidentifiedImageError
import logging

logger = logging.getLogger(__name__)

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
            return self.profile_picture.url + "?c_fill,g_face,h_300,w_300"
        return f"{settings.MEDIA_URL}profile_pics/default.png"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.profile_picture:
            try:
                if isinstance(self.profile_picture.storage, default_storage.__class__):
                    if self.profile_picture.storage.exists(self.profile_picture.name):
                        img_path = self.profile_picture.path
                        with Image.open(img_path) as img:
                            if img.height > 300 or img.width > 300:
                                img.thumbnail((300, 300))
                                img.save(img_path)
            except Exception as e:
                logger.error(f"Error processing profile picture: {e}")


class MyModel(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.name