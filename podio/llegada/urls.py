from . import views
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('race/<int:race_id>', views.race, name='race_id'),
    path('race/<int:race_id>/register_athlete/<int:athlete_id>', views.register_new_athlete, name='register_athlete'),
    path('results/<int:race_id>/<int:category_id>', views.results_per_category, name='results'),
    path('registration/login/', auth_views.LoginView.as_view(template_name='llegada/registration/login.html'), name='login'),
    path('registration/signup/', views.signup, name='signup'),
    path('registration/password_reset/', auth_views.PasswordResetView.as_view(template_name='llegada/registration/login.html'), name='password_reset')
]
