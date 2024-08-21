from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
import uuid


class CustomUserManager(UserManager):
    def create_user(self, username, **extra_fields):
        user = super().create_user(username=username, **extra_fields)
        Profile.objects.create(user=user, first_name=username)
        return user

    def create_superuser(self, username, **extra_fields):
        user = super().create_superuser(username=username, **extra_fields)
        Profile.objects.create(user=user, first_name=username)
        return user


class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    objects = CustomUserManager()


class Profile(models.Model):
    MALE = "M"
    FEMALE = "F"
    OTHER = "O"
    GENDER_CHOICES = [
        (MALE, "Male"),
        (FEMALE, "Female"),
        (OTHER, "Other"),
    ]
    
    PVT = "pvt"
    PUB = "pub"
    PRIVACY_CHOICES = [
        (PVT, "Private"),
        (PUB, "Public")
    ]
    
    first_name = models.CharField(max_length=255, default='')
    second_name = models.CharField(max_length=255, default='', blank=True, null=True)
    last_name = models.CharField(max_length=255, default='', blank=True, null=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile', primary_key=True, editable=False)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default=OTHER)
    nationality = models.CharField(max_length=255, default="International")
    github = models.URLField(max_length=255, default="", blank=True)
    linkedin = models.URLField(max_length=255, default="", blank=True)
    privacy_status = models.CharField(max_length=3, default=PUB, choices=PRIVACY_CHOICES)
    #TODO: Add pfp field
    
    def __str__(self) -> str:
        return f"{self.first_name}:{self.user.id}"
    

class Project(models.Model):
    pid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    leader = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='projects_led')
    title = models.CharField(max_length=255)
    start_date = models.DateField(auto_now_add=True)
    objective = models.TextField(max_length=1000)
    documentation = models.TextField(max_length=50000)
    is_open = models.BooleanField(default=True)
    #TODO: Add panel_img field
    
    
class ProjectContributorMap(models.Model):
    # * Basic: Does not have rights to CUD modules or CUD documentation
    # * Scribe: Does not have rights to CUD modules but can CUD documentation
    # * Admin: Has rights to CUD modules and documentation
    BASIC = "B"
    SCRIBE = "S"
    ADMIN = "A"
    ACCESS_CHOICES = [
        (BASIC, "Basic"),
        (SCRIBE, "Scribe"),
        (ADMIN, "Admin"),
    ]
    
    pid = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='contributors')
    uid = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='projects')
    is_super = models.BooleanField(default=False)
    access = models.CharField(max_length=1, choices=ACCESS_CHOICES, default=BASIC)
