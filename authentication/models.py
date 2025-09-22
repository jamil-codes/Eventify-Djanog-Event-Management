from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from PIL import Image
from django.core.files.base import ContentFile
from io import BytesIO


class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('organizer', 'Organizer'),
        ('attendee', 'Attendee'),
    ]

    name = models.CharField(_("Full Name"), max_length=300, blank=False)
    email = models.EmailField(_("Email address"), unique=True)

    role = models.CharField(
        max_length=20, choices=ROLE_CHOICES, default='attendee'
    )
    tagline = models.CharField(_("Tagline"), max_length=150, blank=True)
    description = models.TextField(_("Description"), blank=True)
    following = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='followers',
        blank=True
    )
    profile_pic = models.ImageField(
        upload_to='profiles/',
        blank=True,
        null=True
    )

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = self.username.lower().capitalize()
        super().save(*args, **kwargs)

        if self.profile_pic:
            img = Image.open(self.profile_pic.path)

            # Resize but keep quality (e.g., max 500x500)
            max_size = (500, 500)
            img.thumbnail(max_size, Image.Resampling.LANCZOS)

            # Save back to same path
            img.save(self.profile_pic.path, format="JPEG", quality=90)

    def __str__(self):
        return f'{self.name} ({self.username})'
