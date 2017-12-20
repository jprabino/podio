import re
import handler.handler as hd


df = hd.init_dataframe()

categories = hd.get_categories(df)
for cat in categories:
    print (cat)
    cat_match = re.match(r"(.*)+?:.*(\d{2}).*[aA]?(\d{2})?.*años",cat)
    if cat_match:
        print (cat_match.groups())