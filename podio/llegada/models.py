
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
    age = models.IntegerField()
    gender = models.CharField(max_length=1, choices=GENDER, default='F')

    def __str__(self):
        return '{}, {}'.format(self.last_name, self.first_name)

class TimeRecord(models.Model):
    """
    TimeRecord for each race for a given athlete
    """
    athlete = models.ForeignKey('Athlete', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    race = models.ForeignKey('Race', on_delete=models.CASCADE)
    time_record = models.DurationField(default=td(seconds=0))

    def __str__(self):
         return 'Results for {}, at {}'.format(self.athlete, self.race)

class Category(models.Model):
    GENDER = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('C', 'Children'),
        ('O', 'Other')
    )
    description = models.CharField(max_length=200)
    gender = models.CharField(max_length=1, choices=GENDER, default='F')
    low_age = models.IntegerField()
    high_age = models.IntegerField()

    def __str__(self):
        return "{} - {}".format(self.description, self.get_gender_display())

class Registered_Athlete(models.Model):
    """
    Once an athlete is registered, it has a Registration Number and a Category
    """
    reg_id = models.AutoField(primary_key=True)
    athlete = models.OneToOneField(to=Athlete, on_delete=models.CASCADE)
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE)

    def __str__(self):
        return 'N° {} -  {}, {}'.format(self.reg_id, self.athlete.last_name,
                                                           self.athlete.first_name)

class Race(models.Model):

    name = models.CharField(max_length=200, unique=True)
    place = models.CharField(max_length=200)
    date = models.DateField(default=timezone.datetime.today)
    init_time = models.DateTimeField(null=True, blank=True)
    length = models.IntegerField(default=1000)
    available_categories = models.ManyToManyField(to=Category, )
    reg_athletes = models.ManyToManyField(to=Registered_Athlete, )
    ended = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def end_race(self):
        self.ended = True

    def resume_race(self):
        self.ended = False

    def get_results(self):
        if not self.ended:
            raise AttributeError('Race has not ended')


    def get_category(self, age, gender):
        """
        Returns the available category given the age and gender of the athlete
        
        :param age:  Integer, the age of the athlete
        :param gender: Choice: M,F,C, O
        :return: Category object, raise attribute error if no category is available.
        """


        avc = self.available_categories.filter(gender=gender).order_by('high_age')

        for cat in avc:
            if age <= cat.high_age:
                return cat
        raise AttributeError("No Category for age: {}, {}".format(age, gender.get_gender_display()))