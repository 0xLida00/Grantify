from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
import cloudinary.uploader
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


    def save(self, *args, **kwargs):
        if self.profile_picture and not self.profile_picture.name.startswith("http"):
            try:
                upload_result = cloudinary.uploader.upload(
                    self.profile_picture.file,
                    folder="profile_pics/",
                    public_id=f"profile_pics/{self.username}_profile_picture",
                    overwrite=True,
                    resource_type="image"
                )
                self.profile_picture.name = upload_result["secure_url"]
            except Exception as e:
                logger.error(f"Error uploading profile picture to Cloudinary: {e}")
                raise ValueError("Failed to upload profile picture to Cloudinary.")

        super().save(*args, **kwargs)


class MyModel(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/', blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.image and not self.image.name.startswith("http"):
            try:
                upload_result = cloudinary.uploader.upload(
                    self.image.file,
                    folder="images/",
                    public_id=f"images/{self.name}_image",
                    overwrite=True,
                    resource_type="image"
                )
                self.image.name = upload_result["secure_url"]
            except Exception as e:
                logger.error(f"Error uploading image to Cloudinary: {e}")
                raise ValueError("Failed to upload image to Cloudinary.")

        super().save(*args, **kwargs)