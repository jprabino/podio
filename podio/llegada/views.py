
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User

from .forms import SignUpForm
from .models import Registered_Athlete, Race, Category, TimeRecord, Athlete
from .tokens import account_activation_token

from rest_framework.decorators import api_view
# Create your views here.


# def index(request):
#     return render(request, 'llegada/index.html', {'project_name': 'podio primer version',})

# def signup(request):
#     if request.method == 'POST':
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.is_active = False
#             user.save()
#             current_site = get_current_site(request)
#             subject = 'Activate Your MySite Account'
#             message = render_to_string('llegada/account_activation_email.html', {
#                 'user': user,
#                 'domain': current_site.domain,
#                 'uid': '{}'.format(urlsafe_base64_encode(force_bytes(user.pk))).replace('b', '', 1).replace("'", ""),
#                 'token': account_activation_token.make_token(user),
#             })
#             user.email_user(subject, message)
#             return redirect('account_activation_sent')
#     else:
#         form = SignUpForm()
#     return render(request, 'llegada/registration/signup.html', {'form': form})

# def account_activation_sent(request):
#     return render(request, 'llegada/registration/account_activation_sent.html')

# def activate(request, uidb64, token):
#     try:
#         uid = force_text(urlsafe_base64_decode(uidb64))
#         user = User.objects.get(pk=uid)
#     except (TypeError, ValueError, OverflowError, ):
#         user = None

#     if user is not None and account_activation_token.check_token(user, token):
#         user.is_active = True
#         user.profile.email_confirmed = True
#         user.save()
#         login(request, user)
#         return redirect('index')
#     else:
#         return render(request, 'llegada/registration/account_activation_invalid.html')


# # def race(request, race_id):

# #     race_obj = get_object_or_404(Race, id=race_id)
# #     try:
# #         reg_athletes = Registered_Athlete.objects.filter(race=race_obj)

# #     except ObjectDoesNotExist:
# #         return HttpResponse('No Reg Athletes for race {}'.format(race_obj.name))

# #     return render(request, 'llegada/race.html', {'race': race_obj, 'reg_athletes': reg_athletes})

# def results_summary_per_category(request, race_id):
#     """
    
#     :param request: 
#     :param race_id: id for the race 
#     :return: 
#     """
#     return

# def results_per_category(request, race_id, category_id):
#     """
#     Returns the view of all the results given a race and a category
#     :param request:
#     :param race_id:
#     :param category_id:
#     :return:
#     """
#     race_obj = get_object_or_404(Race, id=race_id)
#     category_obj = get_object_or_404(Category, id=category_id)

#     reg_athletes = Registered_Athlete.objects.filter(race=race_obj, category=category_obj).values('athlete')

#     if not reg_athletes:
#         return render(request, 'llegada/results.html', {'results': [], 'category': category_obj})

#     time_records = TimeRecord.objects.filter(athlete__in=reg_athletes)

#     return render(request, 'llegada/results.html', {'results': time_records, 'category': category_obj})

# def register_new_athlete(request, athlete_id, race_id):
#     """
#     Adds the Athlete to a Race, assigning a category 
#     :param request: 
#     :param athlete_id: Integer, id of the athelte
#     :param race_id: Integer, id of the race.
#     :return: 
#     """

#     athlete = Athlete.objects.get(id=athlete_id)
#     race = Race.objects.get(id=race_id)

#     category = race.get_category(athlete.age, athlete.gender)

#     try:
#         registered_athlete = Registered_Athlete.objects.create(athlete=athlete,race=race,category=category)
#         registered_athlete.save()
#         race.reg_athletes.add(registered_athlete)
#         race.save()

#     except IntegrityError:
#         registered_athlete = Registered_Athlete.objects.get(athlete = athlete)
#         return render(request, 'llegada/new_register.html', {'new_register': False,
#                                                              'reg_ath': registered_athlete, 'race':race})
#     return render(request, 'llegada/new_register.html', {'new_register': True,
#                                                          'reg_ath': registered_athlete, 'race':race})

# def user_login(request):
#     username = request.POST['username']
#     password = request.POST['password']
#     user = authenticate(request, username=username, password=password)
#     if user is not None:
#         login(request, user)
#         render(request, reverse('index'))
#     else:
#         render(request, reverse('index'))

from django.contrib.auth.models import User, Group
from rest_framework import viewsets,permissions
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from .serializers import UserSerializer, GroupSerializer, AthleteSerializer, RaceSerializer, CategorySerializer
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from datetime import datetime as dt

from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.response import Response
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """    
    permission_classes = [permissions.IsAuthenticated, TokenHasScope]
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class AthleteViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Athlete.objects.all()
    serializer_class = AthleteSerializer

class RaceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    queryset = Race.objects.all()
    serializer_class = RaceSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

@csrf_exempt
@api_view(["GET"])
def sample_api(request):
    data = {'sample_data': 123}
    return Response(data, status=HTTP_200_OK)

@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key},
                    status=HTTP_200_OK)

@api_view(['PUT'])
def start_race(request, race_id):
    """
    set the starttime for the race
    """
    try:
        race_obj = Race.objects.get(pk=race_id)
    except Race.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if race_obj.init_time and request.data.get('override')!='true':
        return Response({'error': 'Race {} already initiated'.format(race_obj)}, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'PUT':
        race_serializer = RaceSerializer(race_obj, data={"init_time":dt.now().strftime("%Y-%m-%dT%H:%M:%S")}, partial=True)#YYYY-MM-DDThh:mm:ss.sTZD)})
        if race_serializer.is_valid():
            race_serializer.save()
            return Response(race_serializer.data)

        return Response(race_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def race_list(request):
    """
    Gets the list of races or creates a new one
    """

    if request.method == 'GET':
        races = Race.objects.all()
        race_serializer = RaceSerializer(races, many=True, context={'request':request})
        return Response(race_serializer.data )
    return Response({}, status=status.HTTP_400_BAD_REQUEST)

def getter_poster(request, obj_class, class_serializer):
    """
    Generic method to get / post single entity
    """

    if request.method == 'GET':
        try:
            pk_id = request.data['id']
            obj = obj_class.objects.get(pk=pk_id)
            obj_serializer = class_serializer(obj, context={'request':request})
            return Response(obj_serializer.data)
        except obj_class.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        obj_serializer = class_serializer(data=request.data, context={'request':request})
        if obj_serializer.is_valid():
            obj_serializer.save()
            return Response(obj_serializer.data, status=status.HTTP_201_CREATED)
        return Response(obj_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','POST'])
def race(request):

    return getter_poster(request, Race, RaceSerializer)


@api_view(['GET','POST'])
def athlete(request):

    return getter_poster(request, Athlete, AthleteSerializer)

