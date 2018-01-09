from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from .models import Registered_Athlete, Race, Category, TimeRecord
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

def results_summary_per_category(request, race_id):
    return

def results_per_category(request, race_id, category_id):
    """
    Returns the view of all the results given a race and a category
    :param request:
    :param race_id:
    :param category_id:
    :return:
    """
    race_obj = get_object_or_404(Race, id=race_id)
    category_obj = get_object_or_404(Category, id=category_id)

    reg_athletes = Registered_Athlete.objects.filter(race=race_obj, category=category_obj)

    if not reg_athletes:
        return HttpResponse('No registered athletes for category "{}" in race: "{}"'.format(category_obj, race_obj))

    time_records = TimeRecord.objects.filter(result_athlete__in=reg_athletes)

    return HttpResponse(time_records)

