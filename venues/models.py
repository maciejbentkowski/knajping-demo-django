from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Avg, Count


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

    def avg_rating(self) -> str:
        rating_data = Review.objects.filter(venue=self).aggregate(
            avg_quality=Avg('rating__quality_rating'),
            avg_service=Avg('rating__service_rating'),
            avg_atmosphere=Avg('rating__atmosphere_rating'),
            avg_value=Avg('rating__value_rating'),
            avg_availability=Avg('rating__availability_rating'),
            avg_uniqueness=Avg('rating__uniqueness_rating'),
            total_ratings=Count('rating_id')
        )
        total_ratings = rating_data['total_ratings']
    
        if total_ratings == 0:
            return None
        
        avg_venue_rating = (
            rating_data['avg_quality'] +
            rating_data['avg_service'] +
            rating_data['avg_atmosphere'] +
            rating_data['avg_value'] +
            rating_data['avg_availability'] +
            rating_data['avg_uniqueness']
        ) / 6
        
        return f"{avg_venue_rating:.2f} / 6"

    
class Comment(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name="comments")

    def __str__(self):
        return self.text

    def user_avg_rating(self) -> str:
        rating_data = Review.objects.filter(venue=self.venue, user=self.user).aggregate(
            avg_quality=Avg('rating__quality_rating'),
            avg_service=Avg('rating__service_rating'),
            avg_atmosphere=Avg('rating__atmosphere_rating'),
            avg_value=Avg('rating__value_rating'),
            avg_availability=Avg('rating__availability_rating'),
            avg_uniqueness=Avg('rating__uniqueness_rating'),
            total_ratings=Count('rating_id')
        )
        total_ratings = rating_data['total_ratings']
    
        if total_ratings == 0:
            return None
        
        avg_venue_rating = (
            rating_data['avg_quality'] +
            rating_data['avg_service'] +
            rating_data['avg_atmosphere'] +
            rating_data['avg_value'] +
            rating_data['avg_availability'] +
            rating_data['avg_uniqueness']
        ) / 6
        
        return f"{avg_venue_rating:.2f}"


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
    
    def avg(self) -> str:
        avg_value = str((self.quality_rating + self.service_rating + self.atmosphere_rating + self.value_rating + self.availability_rating + self.uniqueness_rating)/6)
        return avg_value
    
      
class Menu(models.Model):
    name = models.CharField()
    description = models.TextField()
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name='menus')
    
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

    def avg_rating(self) -> float:
        rating = self.rating
        total = sum([
                rating.quality_rating, 
                rating.service_rating, 
                rating.atmosphere_rating, 
                rating.value_rating, 
                rating.availability_rating, 
                rating.uniqueness_rating
                ])
        avg = total / 6
        return round(avg, 2)   

    
    def rating_list(self) -> dict:
        rating = self.rating
        return {
            'Quality Rating': rating.quality_rating,
            'Service Rating': rating.service_rating,
            'Atmosphere Rating': rating.atmosphere_rating,
            'Value Rating': rating.value_rating,
            'Availability Rating': rating.availability_rating,
            'Uniqueness Rating': rating.uniqueness_rating
        }