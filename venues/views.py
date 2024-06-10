from django.http import Http404
from django.shortcuts import render, redirect

from .models import Venue
from .forms import VenueForm
# Create your views here.


def index(request):
    venues_all = Venue.objects.all()
    context = {'venues_all': venues_all}
    return render(request, 'venues/index.html', context)


def detail(request, pk):
    try:
        venue = Venue.objects.get(id = pk)
    except Venue.DoesNotExist:
        raise Http404("Venue does not exist")
    return render(request, "venues/detail.html", {"venue": venue})


def venues(request):
    venues = Venue.objects.all()
    context = {'venues': venues}
    return render(request, 'venues/venues.html', context)


def create_venue(request):
    form = VenueForm()
    if request.method == 'POST':
        form = VenueForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('venues:venues')
    context = {'form': form}
    return render(request, 'venues/venue_form.html', context)


def update_venue(request, pk):
    venue = Venue.objects.get(id=pk)
    form = VenueForm(instance=venue)

    if request.method == 'POST':
        form = VenueForm(request.POST, instance=venue)
        if form.is_valid():
            form.save()
            return redirect('venues:venues')

    context = {'form': form}
    return render(request, 'venues/venue_form.html', context)


def delete_venue(request, pk):
    venue = Venue.objects.get(id=pk)
    if request.method == 'POST':
        venue.delete()
        return redirect('venues:venues')
    return render(request, 'venues/delete.html', {'obj': venue})
