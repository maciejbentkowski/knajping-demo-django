from .models import Venue, Rating, Comment, Category
from django.forms import ModelForm, TextInput, CharField, BooleanField, CheckboxInput, MultipleChoiceField,SelectMultiple, ModelChoiceField, ModelMultipleChoiceField, CheckboxSelectMultiple, RadioSelect



class VenueForm(ModelForm):

    name = CharField(required=True, label="Nazwa:", widget=TextInput(attrs={'class':' flex mt-1 mb-3 shadow w-full leading-tight'}))
    categories = ModelMultipleChoiceField(required=False, label="Kategorie:",queryset= Category.objects.all(), widget=CheckboxSelectMultiple(attrs={'class': 'my-2 pl-2 shadow '}))
    is_active = BooleanField(required=False, label='Czy twój lokal jest aktywny?', widget=CheckboxInput(attrs={'class':'pl-2'}))

    class Meta:
        model = Venue
        exclude = ('owner',)
        
    field_order = ['name', 'categories']
    
    
class RatingForm(ModelForm):
    class Meta:
        model = Rating
        fields = ['rating']
        
class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text']