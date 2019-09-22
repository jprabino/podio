from . import views as llegada_views
from django.conf.urls import url
from django.urls import path, include
from django.contrib.auth import views as auth_views
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

urlpatterns = [
    path('rest', include(router.urls)),
    path('', llegada_views.index, name='index'),
    path('race/<int:race_id>', llegada_views.race, name='race_id'),
    path('race/<int:race_id>/register_athlete/<int:athlete_id>', llegada_views.register_new_athlete, name='register_athlete'),
    path('results/<int:race_id>/<int:category_id>', llegada_views.results_per_category, name='results'),
    url(r'^account_activation_sent/$', llegada_views.account_activation_sent, name='account_activation_sent'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        llegada_views.activate, name='activate'),
    path('registration/login/', auth_views.LoginView.as_view(template_name='llegada/registration/login.html'), name='login'),
    path('registration/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('registration/signup/', llegada_views.signup, name='signup'),
    path('registration/password_reset/', auth_views.PasswordResetView.as_view(template_name='llegada/registration/login.html'), name='password_reset')
]
