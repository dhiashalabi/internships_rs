from django.db import models
from internships.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class UserProfileItem(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    profile_id = models.IntegerField()
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255, null=True)
    location = models.CharField(max_length=255, null=True)
    details = models.TextField(null=True)
    url = models.URLField(null=True)

    def __str__(self):
        return f"{self.user_profile.user.username} - {self.title}"
