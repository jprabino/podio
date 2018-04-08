
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User

from .forms import SignUpForm
from .models import Registered_Athlete, Race, Category, TimeRecord, Athlete
from .tokens import account_activation_token
# Create your views here.


def index(request):
    return render(request, 'llegada/index.html', {'project_name': 'podio primer version',})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your MySite Account'
            message = render_to_string('account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return redirect('account_activation_sent')
    else:
        form = SignUpForm()
    return render(request, 'llegada/registration/signup.html', {'form': form})

def account_activation_sent(request):
    return render(request, 'llegada/registration/account_activation_sent.html')

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'account_activation_invalid.html')


def race(request, race_id):

    race_obj = get_object_or_404(Race, id=race_id)
    try:
        reg_athletes = Registered_Athlete.objects.filter(race=race_obj)

    except ObjectDoesNotExist:
        return HttpResponse('No Reg Athletes for race {}'.format(race_obj.name))

    return render(request, 'llegada/race.html', {'race': race_obj, 'reg_athletes': reg_athletes})

def results_summary_per_category(request, race_id):
    """
    
    :param request: 
    :param race_id: id for the race 
    :return: 
    """
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

    reg_athletes = Registered_Athlete.objects.filter(race=race_obj, category=category_obj).values('athlete')

    if not reg_athletes:
        return render(request, 'llegada/results.html', {'results': [], 'category': category_obj})

    time_records = TimeRecord.objects.filter(athlete__in=reg_athletes)

    return render(request, 'llegada/results.html', {'results': time_records, 'category': category_obj})

def register_new_athlete(request, athlete_id, race_id):
    """
    Adds the Athlete to a Race, assigning a category 
    :param request: 
    :param athlete_id: Integer, id of the athelte
    :param race_id: Integer, id of the race.
    :return: 
    """

    athlete = Athlete.objects.get(id=athlete_id)
    race = Race.objects.get(id=race_id)

    category = race.get_category(athlete.age, athlete.gender)

    try:
        registered_athlete = Registered_Athlete.objects.create(athlete=athlete,race=race,category=category)
        registered_athlete.save()
        race.reg_athletes.add(registered_athlete)
        race.save()

    except IntegrityError:
        registered_athlete = Registered_Athlete.objects.get(athlete = athlete)
        return render(request, 'llegada/new_register.html', {'new_register': False,
                                                             'reg_ath': registered_athlete, 'race':race})
    return render(request, 'llegada/new_register.html', {'new_register': True,
                                                         'reg_ath': registered_athlete, 'race':race})

# def user_login(request):
#     username = request.POST['username']
#     password = request.POST['password']
#     user = authenticate(request, username=username, password=password)
#     if user is not None:
#         login(request, user)
#         render(request, reverse('index'))
#     else:
#         render(request, reverse('index'))