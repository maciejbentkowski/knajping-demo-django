from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Avg


class Category(models.Model):

    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "categories"


class Venue(models.Model):
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)
    categories = models.ManyToManyField(Category, related_name="venues")
    owner = models.ForeignKey(User, 
                              on_delete=models.SET_DEFAULT,
                              default=None)
    
    def __str__(self):
        return self.name
    
    def average_rating(self) -> float:
        return Rating.objects.filter(venue=self).aggregate(Avg("rating"))['rating__avg']
    
    def rating(self) -> int:
        return Rating.objects.filter(venue=self)
    

    
class Comment(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name="comments")

    def __str__(self):
        return self.text
    
    def user_rating(self) -> int:
        return Rating.objects.get(user=self.user, venue=self.venue).rating
    

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
    rating = models.IntegerField(
        validators=[MaxValueValidator(6), MinValueValidator(1)],
        choices= {"None":0, "1":1, "2":2, "3":3, "4":4, "5":5, "6":6},
        default=0)
        
    def __str__(self):
        return f"{self.venue.name}: {self.rating}"
    
        
    def user_individual_rating(user, venue) -> int:
        try:
            return Rating.objects.get(user=user, venue=venue).rating
        except Rating.DoesNotExist:
            return None
        
class Menu(models.Model):
    name = models.CharField()
    description = models.TextField()
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.name}  ({self.description})"
    
    def menu_items_all(self):
        return MenuItems.objects.filter(menu = self)
    
class MenuItems(models.Model):
    name = models.CharField()
    description = models.TextField()
    price = models.FloatField()
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        verbose_name_plural = "Menu Items"
        