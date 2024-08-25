import pytest
from django.contrib.auth import get_user_model
from venues.models import Venue, Category
from venues.tests.factories import (UserFactory, 
                                    VenueFactory, 
                                    RatingFactory, 
                                    CategoryFactory)

@pytest.mark.django_db()
class TestVenueModel():
   
   def test_venue_creation(self):
      VenueFactory()
      
      assert Venue.objects.all().count() == 1
   
   def test_str_method(self):
      user = UserFactory()
      venue = VenueFactory(name="Test Venue")
      assert str(venue) == "Test Venue"
      
   def test_rating_method(self):
      venue = VenueFactory()
      rating1 = RatingFactory(venue=venue)
      rating2 = RatingFactory(venue=venue)
        
      ratings = venue.rating()
        
      assert ratings.count() == 2
      assert list(ratings) == [rating1, rating2]
      
   def test_average_rating(self):
      venue = VenueFactory()
      RatingFactory(venue = venue, rating = 4)
      RatingFactory(venue = venue, rating = 2)
      expected_average = 3.0  # (4 + 2) / 2
      assert venue.average_rating() == expected_average
      
   def test_average_rating_no_ratings(self):
        venue = VenueFactory()
        assert venue.average_rating() is None
   
   def test_owner_foreign_key(self):
      user = UserFactory()
      venue = VenueFactory(owner=user)
      assert venue.owner == user
      
   def test_many_to_many_categories(self):
      category1 = CategoryFactory()
      category2 = CategoryFactory()
      venue = VenueFactory(categories = [category1, category2])  
      print(venue)
        
      assert venue.categories.count() == 2
      assert list(venue.categories.all()) == [category1, category2]

   def test_owner_foreign_key(self):
      user = UserFactory()
      venue = VenueFactory(owner=user)
        
      assert venue.owner == user
      
@pytest.mark.django_db()   
class TestCategoryModel():
   
   def test_category_creation(self):
      CategoryFactory()
      
      assert Category.objects.all().count() == 1
      
   def test_str_method(self):
      category = CategoryFactory(name="Test Category")
      assert str(category) == "Test Category"