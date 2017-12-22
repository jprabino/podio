import re
import handler.handler as hd


df = hd.init_dataframe()

categories = hd.get_categories(df)

def cat_field_dict(pk, desc,low,high):

    return {
            "model": "llegada.Category",
            "pk": pk,
            "fields": {
                "description": desc,
                "low_age": low,
                "high_age": high,

                }
            }
fixtures = []
with open('/home/juan/workspace/dev/podio/podio/llegada/fixtures/llegada_fixtures.json','w') as fix_file:
    pk=0
    for cat in categories:
        same_cat = re.match(r'(Master\s[A-Z])\s?:\s?(\d*)\s[aA]\s(\d*)', cat) or \
                   re.match(r'(Juveniles\s[a-z])\s?:\s?(\d*)\s[aA]\s(\d*)', cat) or \
                   re.match(r'(Pre-m\wster):\s?(\d*)\s[aA]\s(\d*)', cat)
        menores_cat = re.match(r'Hasta\s(\d*)',cat)
        general_cat = re.match(r'General', cat)
        pk+=1

        if same_cat:
            fixtures.append(cat_field_dict(pk, same_cat.group(1), int(same_cat.group(2)),int(same_cat.group(3))))
        elif menores_cat:
            fixtures.append(cat_field_dict(pk, 'Menores', 0, int(menores_cat.group(1))))
        elif general_cat:
            fixtures.append(cat_field_dict(pk, general_cat.group(0), 0, 120))
    fix_file.write(str(fixtures))



