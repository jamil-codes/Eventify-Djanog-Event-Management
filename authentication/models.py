from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


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

    def __str__(self):
        return f'{self.name} ({self.username})'
