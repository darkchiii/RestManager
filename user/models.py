from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.conf import settings

class Business(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                  related_name='businesses')
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
            return reverse('business_detail', kwargs={'pk': self.pk})

class UserProfile(models.Model):
    EMPLOYER = 'EMPLOYER'
    EMPLOYEE = 'EMPLOYEE'
    ROLE_CHOICES = [
        (EMPLOYER, 'Pracodawca'),
        (EMPLOYEE, 'Pracownik'),
    ]
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                related_name="profile")
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    business = models.ForeignKey(Business, null=True, blank=True, on_delete=models.SET_NULL,
                                 related_name="employees")

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"

    def get_absolute_url(self):
        return reverse('profile_detail', kwargs={'pk': self.pk})
