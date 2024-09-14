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
    '''
        def average_rating(self) -> float:
        return Rating.objects.filter(venue=self).aggregate(Avg("rating"))['rating__avg']
    
        def rating(self) -> int:
        return Rating.objects.filter(venue=self)
    
    '''


    
class Comment(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name="comments")

    def __str__(self):
        return self.text
    '''
    def user_rating(self) -> int:
        return Rating.objects.get(user=self.user, venue=self.venue).rating

    '''



class Rating(models.Model):
    quality_rating = models.IntegerField(
        validators=[MaxValueValidator(6), MinValueValidator(1)],
        default=0)
    
    service_rating = models.IntegerField(
        validators=[MaxValueValidator(6), MinValueValidator(1)],
        default=0)
    
    atmosphere_rating = models.IntegerField(
        validators=[MaxValueValidator(6), MinValueValidator(1)],
        default=0)
    
    value_rating = models.IntegerField(
        validators=[MaxValueValidator(6), MinValueValidator(1)],
        default=0)
    
    availability_rating = models.IntegerField(
        validators=[MaxValueValidator(6), MinValueValidator(1)],
        default=0)
    
    uniqueness_rating = models.IntegerField(
        validators=[MaxValueValidator(6), MinValueValidator(1)],
        default=0)
    '''
        def __str__(self):
        return Rating.objects.filter(id=self).aggregate(Avg("rating"))['rating__avg']

        
    def user_individual_rating(self) -> int:
        try:
            return Rating.objects.filter(id=self).aggregate(Avg("rating"))['rating__avg']
        except Rating.DoesNotExist:
            return None
    
    '''

 

    
        
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
        
class Review(models.Model):
    title = models.CharField()
    description = models.TextField()
    rating = models.OneToOneField(Rating, on_delete=models.CASCADE, primary_key=True, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
        