from django.shortcuts import render

from venues.models import Venue


# Create your views here.
def index(request):
    venues_list = Venue.objects.all()
    context = {'venues_list': venues_list}
    return render(request, 'core/index.html', context=context)
