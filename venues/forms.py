from .models import Venue, Review, Comment, Category, Rating
from django.forms import ModelForm, TextInput, CharField, BooleanField, CheckboxInput, ModelMultipleChoiceField, CheckboxSelectMultiple, Textarea, ChoiceField, RadioSelect



class VenueForm(ModelForm):

    name = CharField(required=True, label="Nazwa:", widget=TextInput(attrs={'class':' flex mt-1 mb-3 shadow w-full leading-tight'}))
    categories = ModelMultipleChoiceField(required=False, label="Kategorie:",queryset= Category.objects.all(), widget=CheckboxSelectMultiple(attrs={'class': 'my-2 pl-2 shadow '}))
    is_active = BooleanField(required=False, label='Czy twój lokal jest aktywny?', widget=CheckboxInput(attrs={'class':'pl-2'}))

    class Meta:
        model = Venue
        exclude = ('owner',)
        
    field_order = ['name', 'categories']
    
    
class ReviewForm(ModelForm):
    title = CharField(required=True, label="Tytuł:", widget=TextInput(attrs={'class':' flex mt-1 mb-3 shadow w-full leading-tight'}))
    description = CharField(required=True, label="Opis:", widget=Textarea(attrs={'class':' flex mt-1 mb-3 shadow w-full leading-tight'}))
    class Meta:
        model = Review
        exclude = {'user', 'venue', 'rating'}
        
class RatingForm(ModelForm):
    CHOICES = [
        ('nisko', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
    ]
    
    quality_rating = ChoiceField(required=True,
                                 label="Oceń jedzenie",
                                 help_text="Czy jedzenie jest dobrze przygotowane, świeże i smaczne? Jak wyglądają dania? Czy oferta jest zróżnicowana, dostosowana do różnych preferencji dietetycznych?",
                                 choices=CHOICES,
                                 widget=RadioSelect(attrs={'class':' flex mt-1 mb-3 justify-around text-center'}))
    
    service_rating = ChoiceField(required=True,
                                 label="Oceń serwis",
                                 help_text="Czy obsługa jest uprzejma, pomocna i kompetentna? Czy czas oczekiwania jest adekwatny do rodzaju potraw?",
                                 choices=CHOICES,
                                 widget=RadioSelect(attrs={'class':' flex mt-1 mb-3 justify-around text-center'}))
    
    atmosphere_rating = ChoiceField(required=True,
                                    label="Oceń atmosferę",
                                    help_text="Czy restauracja jest estetyczna, wygodna i przytulna? Czy muzyka i światło są odpowiednie, tworząc przyjemny nastrój?",
                                    choices=CHOICES,
                                    widget=RadioSelect(attrs={'class':' flex mt-1 mb-3 justify-around text-center'}))
    
    value_rating = ChoiceField(required=True,
                               label="Oceń jakość",
                               help_text="Czy ceny są odpowiednie do jakości jedzenia i obsługi? Czy lokal i jego otoczenie są zadbane, czyste i schludne?",
                               choices=CHOICES,
                               widget=RadioSelect(attrs={'class':' flex mt-1 mb-3 justify-around text-center'}))
    
    availability_rating = ChoiceField(required=True,
                                      label="Oceń dostępność",
                                      help_text="Czy restauracja znajduje się w dogodnym miejscu? Czy restauracja jest otwarta w dogodnych dla klientów godzinach?",
                                      choices=CHOICES,
                                      widget=RadioSelect(attrs={'class':' flex mt-1 mb-3 justify-around text-center'}))
    
    uniqueness_rating = ChoiceField(required=True,label="Oceń unikalność",
                                    help_text="Czy restauracja oferuje oryginalne dania lub unikalne połączenia smakowe? Czy oferowanie tradycyjne dania są wyjątkowe w swoim smaku?",
                                    choices=CHOICES,
                                    widget=RadioSelect(attrs={'class':' flex mt-1 mb-3 justify-around text-center'}))
    
    class Meta:
        model = Rating
        fields = "__all__"
        
class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text']