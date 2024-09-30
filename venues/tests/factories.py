import factory
from venues.models import Venue, Category, Rating, Comment, Review
from django.contrib.auth import get_user_model
from datetime import datetime


User = get_user_model()

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
    
    username = factory.Faker('name')


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category
    
    name = factory.sequence(lambda n: 'category {}'.format(n))


class VenueFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Venue
        skip_postgeneration_save=True
        
    name = factory.Faker('company')
    is_active = True
    owner = factory.SubFactory(UserFactory)
    @factory.post_generation
    def categories(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        self.categories.add(*extracted)
        
class RatingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Rating
        
    quality_rating = factory.Faker('random_int', min=1, max=6)
    service_rating = factory.Faker('random_int', min=1, max=6)
    atmosphere_rating = factory.Faker('random_int', min=1, max=6)
    value_rating = factory.Faker('random_int', min=1, max=6)
    availability_rating = factory.Faker('random_int', min=1, max=6)
    uniqueness_rating = factory.Faker('random_int', min=1, max=6)
    
class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Comment
    text = factory.Faker('text', max_nb_chars=50)
    created_at = datetime.now()
    user = factory.SubFactory(UserFactory)
    venue = factory.SubFactory(VenueFactory)
    
    
class ReviewFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Review
        
    title = factory.Faker('text', max_nb_chars=25)
    description = factory.Faker('text', max_nb_chars=150)
    rating = factory.SubFactory(RatingFactory)
    user = factory.SubFactory(UserFactory)
    venue = factory.SubFactory(VenueFactory)
    
    