from django.urls import path
from . import views

app_name = "venues"

urlpatterns = [
    path('', views.venues, name='venues'),
    path('<int:venue_id>', views.detail, name='detail'),
]