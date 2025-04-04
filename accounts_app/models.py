# accounts_app/models.py
from django.conf import settings
from django.core.files.storage import default_storage
from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image

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
        """Return profile picture URL or default image."""
        if self.profile_picture and self.profile_picture.storage.exists(self.profile_picture.name):
            return self.profile_picture.url
        return f"{settings.MEDIA_URL}profile_pics/default.png"

    def save(self, *args, **kwargs):
        """Resize profile picture to 300x300 pixels if necessary."""
        super().save(*args, **kwargs)
        if self.profile_picture and self.profile_picture.storage.exists(self.profile_picture.name):
            try:
                img_path = self.profile_picture.path
                with Image.open(img_path) as img:
                    if img.height > 300 or img.width > 300:
                        img.thumbnail((300, 300))
                        img.save(img_path)
            except Exception as e:
                print(f"Error processing profile picture: {e}")