# Generated by Django 2.0 on 2017-12-22 00:19

import llegada.handler.handler as hd

from django.db import migrations
import re



def categories(apps, schema_editor):
    df = hd.init_dataframe()

    categories = hd.get_categories(df)
    Category = apps.get_model('llegada', 'Category')
    for cat in categories:
        same_cat = re.match(r'(Master\s[A-Z])\s?:\s?(\d*)\s[aA]\s(\d*)', cat) or \
                   re.match(r'(Juveniles\s[a-z])\s?:\s?(\d*)\s[aA]\s(\d*)', cat) or \
                   re.match(r'(Pre-m\wster):\s?(\d*)\s[aA]\s(\d*)', cat)
        menores_cat = re.match(r'Hasta\s(\d*)', cat)
        general_cat = re.match(r'General', cat)

        if same_cat:
            cat = Category.objects.create(description=same_cat.group(1), low_age=int(same_cat.group(2)), high_age=int(same_cat.group(3)))
        elif menores_cat:
            cat = Category.objects.create(description='Menores', low_age=0, high_age=int(menores_cat.group(1)))
        elif general_cat:
            cat = Category.objects.create(description='General', low_age=0, high_age=120)
        cat.save()

class Migration(migrations.Migration):

    dependencies = [
        ('llegada', '0001_initial'),
    ]

    operations = [ migrations.RunPython(categories),
    ]
