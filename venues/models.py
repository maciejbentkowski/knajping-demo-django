from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):

    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Venue(models.Model):
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)
    categories = models.ManyToManyField(Category, related_name="venues")

    def __str__(self):
        return self.name


class Comment(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name="comments")

    def __str__(self):
        return self.text
