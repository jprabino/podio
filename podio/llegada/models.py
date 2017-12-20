from django.db import models

# Create your models here.

class Athlete(models.Model):

    id_number = models.IntegerField(unique=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    race = models.ManyToManyField('Race')
    age = models.IntegerField()

    def __str__(self):
        return '{}, {}'.format(self.last_name, self.first_name)

class Category(models.Model):

    description = models.CharField(max_length=200, unique=True)
    low_age = models.IntegerField()
    high_age = models.IntegerField()

    def __str__(self):
        return self.description

class Race(models.Model):

    name = models.CharField(max_length=200, unique=True)
    place = models.CharField(max_length=200)
    date = models.DateField()
    length = models.IntegerField()

    def __str__(self):
        return self.name