
from django.db import models
from django.utils import timezone
# Create your models here.
from datetime import timedelta as td

class Athlete(models.Model):
    GENDER = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    )
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    time_records = models.ManyToManyField('TimeRecord')
    age = models.IntegerField()
    gender = models.CharField(max_length=1, choices=GENDER, default='F')

    def __str__(self):
        return '{}, {}'.format(self.last_name, self.first_name)

class TimeRecord(models.Model):
    """
    TimeRecord for each race for a given athlete
    """
    r_id = models.IntegerField(primary_key=True, )
    result_athlete = models.ForeignKey('Athlete', on_delete=models.CASCADE)
    result_race = models.ForeignKey('Race', on_delete=models.CASCADE)
    time_record = models.DurationField(default=td(seconds=0))

    def __str__(self):
         return 'Results for {}, at {}'.format(self.result_athlete, self.result_race)

class Registered_Athlete(models.Model):
    """
    Once an athlete is registered, there
    """
    ath_id = models.IntegerField
class Category(models.Model):

    description = models.CharField(max_length=200, unique=True)
    low_age = models.IntegerField()
    high_age = models.IntegerField()

    def __str__(self):
        return self.description

class Race(models.Model):

    name = models.CharField(max_length=200, unique=True)
    place = models.CharField(max_length=200)
    date = models.DateField(default = timezone.datetime.today)
    init_time = models.DateTimeField(null=True, blank=True)
    length = models.IntegerField(default=1000)
    available_categories = models.ManyToManyField(to=Registered_Athlete)
    reg_athletes = models.ManyToManyField(to=Athlete)

    def __str__(self):
        return self.name

