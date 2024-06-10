from django.urls import path
from . import views

app_name = "venues"

urlpatterns = [
    path('', views.index, name='index'),
    path('venues/', views.venues, name='venues'),
    path('venues/<int:venue_id>', views.detail, name='detail'),
]