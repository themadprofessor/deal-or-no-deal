from django.db import models


# Create your models here.
class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    deal_id = models.ForeignKey()
    user_id = models.ForeignKey()
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
