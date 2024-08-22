from django.contrib import admin

from venues.models import Venue, Category, Rating

# Register your models here.
admin.site.register(Venue)
admin.site.register(Category)
admin.site.register(Rating)