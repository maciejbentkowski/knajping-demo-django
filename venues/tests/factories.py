import factory
from venues.models import Venue, Category, Rating, Comment
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
        
    rating = factory.Faker('random_int', min=1, max=6)
    user = factory.SubFactory(UserFactory)
    venue = factory.SubFactory(VenueFactory)
    
class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Comment
    text = factory.Faker('text', max_nb_chars=50)
    created_at = datetime.now()
    user = factory.SubFactory(UserFactory)
    venue = factory.SubFactory(VenueFactory)