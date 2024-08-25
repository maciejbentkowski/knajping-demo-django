import factory
from venues.models import Venue, Category, Rating
from django.contrib.auth import get_user_model

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