from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('race/<int:race_id>', views.race, name='id'),
]
