from django.contrib import admin

from venues.models import Venue, Category, Rating, Menu, MenuItems

# Register your models here.
admin.site.register(Venue)
admin.site.register(Category)
admin.site.register(Rating)
admin.site.register(Menu)
admin.site.register(MenuItems)