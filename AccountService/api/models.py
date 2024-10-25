from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    deleted = models.BooleanField(default=False)
    roles = models.JSONField(default=list)

    def save(self, *args, **kwargs):
        clean_roles = list(self.roles)
        clean_roles.append("User")
        self.roles = list(set(clean_roles))
        super().save(*args, **kwargs)


class IssuedToken(models.Model):
    token = models.TextField()
    refresh_token = models.TextField()
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    date_of_issue = models.DateTimeField(auto_now_add=True, blank=True)
    is_invalidated = models.BooleanField(default=False)
