import json

import os
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, username, first_name, last_name, email, password=None, likes=0, authority=False):
        if not email:
            raise ValueError("Users must have an email address")
        if not first_name:
            raise ValueError("Users must have a first name")
        if not last_name:
            raise ValueError("Users must have a last name")

        user = self.model(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            likes=likes,
            authority=False
        )

        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, username, first_name, last_name, email, password=None, likes=0, authority=False):
        if not email:
            raise ValueError("Superusers must have an email address")
        if not first_name:
            raise ValueError("Superusers must have a first name")
        if not last_name:
            raise ValueError("Superusers must have a last name")

        user = self.model(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            likes=likes,
            authority=True
        )

        user.set_password(password)
        user.save(using=self.db)
        return user


# Create your models here.
class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    deal_id = models.ForeignKey('Deal', on_delete=models.CASCADE)
    user_id = models.ForeignKey('User', on_delete=models.CASCADE)
    creation_date = models.DateTimeField()
    content = models.TextField()

    REQUIRED = ['deal_id', 'content']

    def __str__(self):
        return self.content

    def to_json(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        return {
            'id': self.id,
            'deal_id': self.deal_id,
            'user_id': self.user_id,
            'creation_date': self.creation_date,
            'content': self.content
        }


class Category(models.Model):
    REQUIRED = ['id', 'name', 'description']

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=10)
    description = models.TextField()

    def __str__(self):
        return self.name

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }

    def to_json(self):
        return json.dumps(self.to_dict())


class User(AbstractUser):
    username = models.CharField("Username", max_length=128, primary_key=True)
    email = models.CharField("Email", max_length=128)
    first_name = models.CharField("First Name", max_length=30)
    last_name = models.CharField("Last Name", max_length=30)
    likes = models.IntegerField("Number of likes", default=0)
    authority = models.BooleanField(default=False)

    REQUIRED = ['username', 'first_name', 'last_name', 'email', 'password']
    UPDATEABLE = ['first_name', 'last_name', 'email', 'password', 'likes']

    # Unique ID used by Django
    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "email"]

    objects = UserManager()

    def __str__(self):
        return self.username

    @property
    def is_staff(self):
        return self.authority

    @property
    def is_superuser(self):
        return self.authority

    def to_json(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        return {
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'like': self.authority
        }


class Deal(models.Model):
    id = models.AutoField(primary_key=True)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    description = models.TextField()
    price = models.FloatField(default=0.0)
    creation_date = models.DateTimeField(default=timezone.now)
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)
    image_path = models.URLField(default=settings.STATIC_URL + "no-img.png")
    url = models.URLField(blank=True)

    REQUIRED = ['category_id', 'user_id', 'title', 'description', 'price']

    def __str__(self):
        return self.title

    def to_json(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        return {
            'id': self.id,
            'category_id': self.category_id.id,
            'user_id': self.user_id.username,
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'creation_date': self.creation_date.timestamp(),
            'upvotes': self.upvotes,
            'downvotes': self.downvotes,
            'image_path': self.image_path
        }