from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import Http404
from django.contrib.auth.forms import UserCreationForm

from .models import (Venue,
                     Comment,
                     Rating,
                     Review,
                     Menu,
                     MenuItems,)
from .forms import (VenueForm,
                    CommentForm,
                    ReviewForm,
                    RatingForm,
                    MenuForm,
                    MenuItemsFormSet,)


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
    comment_form = CommentForm()
    menus = Menu.objects.filter(venue=venue)
    reviews = Review.objects.filter(venue=venue)
    
    try:
        venue = Venue.objects.get(id=pk)
    except Venue.DoesNotExist:
        raise Http404("Venue does not exist")

    if (venue.owner != request.user) and venue.is_active == False:
        messages.error(request, "Ta restauracja nie jest aktywna")
        return redirect('venues:index')
    
    if request.method == 'POST' and 'comment_add' in request.POST:
        Comment.objects.create(
            user=request.user,
            venue=venue,
            text=request.POST.get('text')
        )
        return redirect('venues:detail', pk=venue.pk)

        
    if request.method == 'POST' and 'rating_update' in request.POST:
        Rating.objects.update_or_create(
                user=request.user,
                venue=venue,
                defaults={"rating": request.POST.get('rating')},
            )
        return redirect('venues:detail', pk=venue.pk)


    context = {"venue": venue,
               "comments": comments,
               "comment_form": comment_form,
               "menus":menus,
               "reviews":reviews
               }
    return render(request, "venues/detail.html", context)


def venues(request):
    venues_list = Venue.objects.all()
    context = {'venues': venues_list}
    return render(request, 'venues/venues.html', context)


@login_required(login_url='venues:login')
def create_venue(request):
    purpose = "Dodaj"
    helper_text = "Po stworzeniu swojego lokalu, będzie on widoczny tylko dla Ciebie. Można go aktywować w opcji Edytuj"

    venue_form = VenueForm()
    is_active_field = venue_form.fields['is_active']
    is_active_field.disabled = True
    is_active_field.widget = is_active_field.hidden_widget()
    if request.method == 'POST':
        venue_form = VenueForm(request.POST)
        if venue_form.is_valid():
            venue = venue_form.save(commit=False)
            venue.owner = request.user
            venue.save()
            venue.categories.add(*venue_form.cleaned_data['categories'])
            return redirect('venues:venues')
    context = {'venue_form': venue_form, 'helper_text': helper_text, 'purpose':purpose}
    return render(request, 'venues/venue_form.html', context)


@login_required(login_url='venues:login')
def update_venue(request, pk):
    purpose = "Edytuj"
    venue = Venue.objects.get(id=pk)
    venue_form = VenueForm(instance=venue)
    if venue.owner != request.user:
        messages.error(request, "You can only edit your venues")
        return redirect('venues:index')
    if request.method == 'POST':
        venue_form = VenueForm(request.POST, instance=venue)
        if venue_form.is_valid():
            venue_form.save()
            return redirect('venues:profile', pk=request.user.id)

    context = {'venue_form': venue_form, 'purpose': purpose, 'venue':venue}
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
    
@login_required(login_url='venues:login')
def create_review(request, pk):
    venue = Venue.objects.get(id=pk)
    if (venue.owner != request.user) and venue.is_active == False:
        messages.error(request, "Nie mozesz ocenić nieaktywnej restauracji")
        return redirect('venues:index')
    elif (venue.owner == request.user):
        messages.error(request, "Nie mozesz ocenić swojej restauracji")
        return redirect('venues:detail', pk=pk)
    try:
        review = Review.objects.get(user=request.user.id, venue=pk)
        rating = Rating.objects.get(id = review.rating.id)
    except:
        review = None
        rating = None
    review_form = ReviewForm(instance =review)
    rating_form = RatingForm(instance = rating)
    if request.method == 'POST':
        rating_form = RatingForm(request.POST, instance=rating)
        review_form = ReviewForm(request.POST, instance=review)
        if rating_form.is_valid():
            rating = rating_form.save()
            rating.save()
            if review_form.is_valid():
                review = review_form.save(commit=False)
                review.user = request.user
                review.rating = Rating.objects.get(id=rating.id)
                review.venue = Venue.objects.get(id=pk)
                review.save()
            return redirect('venues:venues')
    context = {'review_form': review_form, 'rating_form': rating_form}
    return render(request, 'venues/review_form.html', context)

@login_required(login_url='venues:login')
def profile(request, pk):
    user = User.objects.get(id = pk)
    venues = Venue.objects.filter(owner = user.id).order_by('-is_active','name')
    reviews = Review.objects.filter(user = user.id)
    avg_rating = Review.avg_rating
    context = {'venues': venues, 'reviews': reviews, 'avg_rating':avg_rating}
    return render(request, 'venues/profile.html', context)

@login_required(login_url='venues:login')
def menu_list(request, pk):
    venue = Venue.objects.get(id=pk)
    menus = venue.menus.all()
    menu_form = MenuForm()
    if request.method == 'POST' and 'menu_add' in request.POST:
        Menu.objects.create(
            name = request.POST.get('name'),
            description=request.POST.get('description'),
            venue=venue
            )
        return redirect('venues:menu', pk=venue.pk)
        
    context = {'venue': venue, 'menus': menus, 'menu_form': menu_form}
    return render(request, 'venues/menu.html', context)

@login_required(login_url='venues:login')
def delete_menu(request, pk):
    menu = Menu.objects.get(id=pk)
    
    if request.user != menu.venue.owner:
        messages.error(request, "You do not have permission to delete this comment")
        return redirect('venues:menu', pk = menu.venue.pk)
    
    if request.method == 'POST':
        menu.delete()
        return redirect('venues:menu', pk = menu.venue.pk)
    else:
        return render(request, 'venues/detail.html') 


def menu_items(request, pk, menu):
    venue = Venue.objects.get(id=pk)
    menu = Menu.objects.get(id=menu)
    formset = MenuItemsFormSet(instance = menu)
    if request.method == 'POST' and 'menu_add_items' in request.POST:
        formset = MenuItemsFormSet(request.POST, instance=menu)
        if formset.is_valid():
            formset.save()
            return redirect('venues:menu', pk=venue.pk)

    context = {'menu': menu, 'formset': formset,}
    return render(request, 'venues/menu_items_form.html', context)