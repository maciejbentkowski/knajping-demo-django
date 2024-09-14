from django.contrib import admin

from venues.models import Venue, Category, Rating, Review, Menu, MenuItems

# Register your models here.
admin.site.register(Venue)
admin.site.register(Category)
admin.site.register(Rating)
admin.site.register(Review)
admin.site.register(Menu)
admin.site.register(MenuItems)