from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import Http404
from django.contrib.auth.forms import UserCreationForm
from .models import Venue, Comment
from .forms import VenueForm


def create_session(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            username == User.objects.get(username=username)
        except Exception:
            messages.error(request, "User does not exist")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('venues:index')
        else:
            messages.error(request, "Invalid username or password")

    context = {'page': page}
    return render(request, "venues/create_session.html", context)


def destroy_session(request):
    logout(request)
    return redirect('venues:index')


def register_user(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('venues:index')
        else:
            messages.error(request, "An error occured")

    context = {'form': form}
    return render(request, 'venues/create_user.html', context)


def index(request):
    venues_all = Venue.objects.all()
    context = {'venues_all': venues_all}
    return render(request, 'venues/index.html', context)


def detail(request, pk):
    venue = Venue.objects.get(pk=pk)
    comments = venue.comments.all()
    try:
        venue = Venue.objects.get(id=pk)
    except Venue.DoesNotExist:
        raise Http404("Venue does not exist")

    if request.method == 'POST':
        Comment.objects.create(
            user=request.user,
            venue=venue,
            text=request.POST.get('text')
        )
        return redirect('venues:detail', pk=venue.pk)

    context = {"venue": venue,
               "comments": comments}
    return render(request, "venues/detail.html", context)


def venues(request):
    venues_list = Venue.objects.all()
    context = {'venues': venues_list}
    return render(request, 'venues/venues.html', context)


@login_required(login_url='venues:login')
def create_venue(request):
    form = VenueForm()
    if request.method == 'POST':
        form = VenueForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('venues:venues')
    context = {'form': form}
    return render(request, 'venues/venue_form.html', context)


@login_required(login_url='venues:login')
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


@login_required(login_url='venues:login')
def delete_venue(request, pk):
    venue = Venue.objects.get(id=pk)
    if request.method == 'POST':
        venue.delete()
        return redirect('venues:venues')
    return render(request, 'venues/delete.html', {'obj': venue})


def delete_comment(request, pk):
    comment = Comment.objects.get(id=pk)

    if request.user != comment.user:
        messages.error(request, "You do not have permission to delete this comment")

    if request.method == 'POST':
        comment.delete()
        return redirect('venues:detail', pk=comment.venue.pk)
    else:
        return render(request, 'venues/detail.html')
