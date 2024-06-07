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
