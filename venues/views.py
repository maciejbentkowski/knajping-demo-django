from django.http import Http404
from django.shortcuts import render

from .models import Venue
# Create your views here.


def venues(request):
    venues_all = Venue.objects.all()
    context = {'venues_all': venues_all}
    return render(request, 'venues/venue.html', context = context)


def detail(request, venue_id):
    try:
        venue = Venue.objects.get(pk=venue_id)
    except Venue.DoesNotExist:
        raise Http404("Venue does not exist")
    return render(request, "venues/detail.html", {"venue": venue})