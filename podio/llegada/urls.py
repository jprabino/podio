from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('race/<int:race_id>', views.race, name='race_id'),
    path('results/<int:race_id>/<int:category_id>', views.results_per_category, name='results'),
]