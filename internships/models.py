from django.utils import timezone
from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    profile = models.ImageField(upload_to="profile", blank=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    country = models.ForeignKey("Country", null=True, blank=True, on_delete=models.CASCADE)
    city = models.ForeignKey("City", null=True, blank=True, on_delete=models.CASCADE)
    location = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    date_joined = models.DateTimeField(default=timezone.now, blank=True)
    GENDER_CHOICES = (
        ("male", "Male"),
        ("female", "Female"),
    )
    gender = models.CharField(
        max_length=15,
        choices=GENDER_CHOICES,
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.username


class Country(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    country = models.ForeignKey(Country, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class InternshipCategory(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class InternshipType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Internship(models.Model):
    title = models.CharField(max_length=255)
    internship_category = models.ForeignKey(
        InternshipCategory,
        null=True,
        on_delete=models.CASCADE,
    )
    internship_type = models.ForeignKey(
        InternshipType,
        null=True,
        on_delete=models.CASCADE,
    )
    description = models.TextField(validators=[MinLengthValidator(100)])
    image = models.ImageField(upload_to="internship", blank=True)
    company = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    country = models.ForeignKey(Country, null=True, on_delete=models.CASCADE)
    city = models.ForeignKey(City, null=True, on_delete=models.CASCADE)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    duration = models.IntegerField(blank=True, null=True)
    stipend = models.IntegerField(blank=True, null=True)
    apply_by = models.DateField(blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class UserInterest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    internships = models.ManyToManyField(Internship, blank=True)

    def __str__(self):
        return self.user.username
