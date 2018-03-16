import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
						'tango_with_django.settings')
						
import django
django.setup()
from rango.models import Category, Page
import random as RNG

def populate():
    categories = [ "Food", "Fashion", "Travel", "Electronics", "Accommodation",
                   "Health and Fitness"]
    users = [ {"fname": "Jason", "lname": "Smith", "email":"jsmith@mail.com",
               "likes":RNG.randint(1,50), "auth":1},
              {"fname": "Jimmy", "lname": "Singer", "email":"jsinger@mail.com",
               "likes":RNG.randint(1,50), "auth":0},
              {"fname": "Liza", "lname": "Harpoon", "email":"lharpoon@mail.com",
               "likes":RNG.randint(1,50), "auth":0},
              {"fname": "Mike", "lname": "Jimson", "email":"mjimson@mail.com",
               "likes":RNG.randint(1,50), "auth":0},
              ]
    deals = [ {"title":"FaT DealS", "desc":"Breakfast buffet with copious amounts of bacon", "category":"Food",
               "price":6.99, "up":RNG.randint(1,100), "down":RNG.randint(1,33)},
              {"title":"Air Jordans", "desc":"Whaddup fams, theres some mad deals on Air Jordans right now go check em out. Don't for get to use your student discount.", "category":"Fashion",
               "price":39.99, "up":RNG.randint(1,100), "down":RNG.randint(1,33)}
              {"title":"iPhone X", "desc":"Apple Genius here, just wanted to inform you guys of the LATEST deals we have at the Apple Store, drop by to pick up your iPhone X now!!!", "category":"Electronics",
               "price":99999.99, "up":RNG.randint(1,100), "down":RNG.randint(1,33)}
              ]
    comments = [ {}]
