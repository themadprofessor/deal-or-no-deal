from django.db import models
from django.utils import timezone


# Create your models here.
class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    deal_id = models.ForeignKey('Deal', on_delete=models.CASCADE)
    user_id = models.ForeignKey('User', on_delete=models.CASCADE)
    creation_date = models.DateTimeField()
    content = models.TextField()

    def __str__(self):
        return self.content


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=10)
    description = models.TextField()

    def __str__(self):
        return self.name


class User(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField("First Name", max_length=30)
    last_name = models.CharField("Last Name", max_length=30)
    email = models.CharField("Email", max_length=128)
    likes = models.IntegerField("Number of likes", default=0)
    authority = models.BooleanField(default=False)

    def __str__(self):
        return self.first_name + " " + self.last_name


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

    def __str__(self):
        return self.title
