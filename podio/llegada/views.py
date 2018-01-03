from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from .models import Registered_Athlete, Race
# Create your views here.


def index(request):

    return render(request, 'llegada/index.html')

def race(request, race_id):

    race_obj = get_object_or_404(Race, id=race_id)
    try:
        reg_athletes = Registered_Athlete.objects.filter(race=race_obj)

    except ObjectDoesNotExist:
        return HttpResponse('No Reg Athletes for race {}'.format(race_obj.name))

    return render(request, 'llegada/race.html', {'race': race_obj, 'reg_athletes': reg_athletes})