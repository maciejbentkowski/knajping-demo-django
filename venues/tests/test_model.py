import pytest
from django.contrib.auth import get_user_model
from venues.models import Venue

User = get_user_model()

@pytest.mark.django_db()
class TestVenueModel():
   
   def test_str_method(self):
      user = User.objects.create(username="testuser")
      venue = Venue.objects.create(name="Test Venue", owner=user)
      assert str(venue) == "Test Venue"
   
   def test_owner_foreign_key(self):
      user = User.objects.create(username="testuser")
      venue = Venue.objects.create(name="Test Venue", owner=user)
      assert venue.owner == user