import pytest
from venues.models import Venue, Category, Comment, Rating, Review
from venues.tests.factories import (UserFactory, 
                                    VenueFactory, 
                                    RatingFactory, 
                                    CategoryFactory,
                                    CommentFactory,
                                    ReviewFactory
                                    )


from django.core.exceptions import ValidationError

@pytest.mark.django_db()
class TestVenueModel():
   
   def test_venue_creation(self):
      VenueFactory()
      
      assert Venue.objects.all().count() == 1
   
   def test_str_method(self):
      venue = VenueFactory(name="Test Venue")
      assert str(venue) == "Test Venue"
      
   
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
      
@pytest.mark.django_db()   
class TestCommentModel():
   
   def test_comment_creation(self):
      CommentFactory()
      
      assert Comment.objects.all().count() == 1
      
   def test_str_method(self):
      comment = CommentFactory(text="Test Comment")
      assert str(comment) == "Test Comment"
      
@pytest.mark.django_db()   
class TestRatingModel():
   
   def setUp(self):
      self.rating = RatingFactory()
   
   def test_rating_validators(self):
      """Test that the validators work for rating fields"""  
      rating = RatingFactory.build()
      rating.quality_rating = 7
      with pytest.raises(ValidationError):
         rating.full_clean() 

@pytest.mark.django_db()   
class TestReviewModel():
   
   def test_review_creation(self):
      ReviewFactory()
      
      assert Review.objects.all().count() == 1
      
   def test_review_avg_rating(self):
      rating = RatingFactory(
         quality_rating=5,
         service_rating=3,
         atmosphere_rating=3,
         value_rating=5,
         availability_rating=2,
         uniqueness_rating=3,
      )
      
      review = ReviewFactory(rating = rating)
      
      expected_avg_rating = round((5 + 3 + 3 + 5 + 2 + 3) / 6, 2)
      assert review.avg_rating() == expected_avg_rating
      
      