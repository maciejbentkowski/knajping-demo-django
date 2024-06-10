from django.urls import path
from . import views

app_name = "venues"

urlpatterns = [
    path('', views.index, name='index'),
    path('venues/', views.venues, name='venues'),
    path('venues/<str:pk>/', views.detail, name='detail'),

    path('create-venue/', views.create_venue, name='create-venue'),
    path('update-venue/<str:pk>/', views.update_venue, name='update-venue'),
    path('delete-venue/<str:pk>/', views.delete_venue, name='delete-venue'),
]