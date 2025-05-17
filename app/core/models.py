from django.db.models import CharField, UUIDField, JSONField, DateTimeField
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)
from uuid import uuid4
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("User must have an email adress")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Creata and return a new superuser"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system"""

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = "email"


STATUS_CHOICES = [
    ("pending", "Pending"),
    ("checked", "Checked"),
    ("rejected", "Rejected"),
]


class Candidate(models.Model):
    id = UUIDField(primary_key=True, default=uuid4, editable=False)
    full_name = CharField(max_length=255, null=False)
    # Dovrebbe essere unico il campo email, ma lo lascio così per celery (In una reale app questo deve essere unique=True)
    email = CharField(max_length=255, null=False)
    status = CharField(choices=STATUS_CHOICES, max_length=20)
    screening_log = JSONField(blank=True, default=dict)
    created_at = DateTimeField(auto_now_add=True)
    update_at = DateTimeField(auto_now=True)
