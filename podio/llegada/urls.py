from django.urls import path
from . import views
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('race/<int:race_id>', views.race, name='race_id'),
    path('race/<int:race_id>/register_athlete/<int:athlete_id>', views.register_new_athlete, name='register_athlete'),
    path('results/<int:race_id>/<int:category_id>', views.results_per_category, name='results'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', auth_views.logout, name='logout'),
]
