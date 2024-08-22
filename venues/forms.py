from django.forms import ModelForm
from .models import Venue, Rating, Comment


class VenueForm(ModelForm):
    class Meta:
        model = Venue
        fields = '__all__'

class RatingForm(ModelForm):
    class Meta:
        model = Rating
        fields = ['rating']
        
class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text']