from . import views as llegada_views
from django.conf.urls import url
from django.urls import path, include
from django.contrib.auth import views as auth_views
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

router = routers.DefaultRouter()
router.register(r'groups', views.GroupViewSet)
router.register(r'race', views.RaceViewSet)
router.register(r'athlete', views.AthleteViewSet)
router.register(r'category', views.CategoryViewSet)
router.register(r'user', views.UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('race/start/<int:race_id>', views.start_race),
    path('race/list', views.race_list),
    path('race', views.race),
    path('athlete', views.athlete),
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
]

# urlpatterns = format_suffix_patterns(urlpatterns)