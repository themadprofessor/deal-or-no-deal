import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
						'deal_or_no_deal.settings')
						
import django
django.setup()
from dondapp.models import *
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
    usernames = [ users[x]["fname"].lower()+users[x]["lname"].lower() for x in range(4)]
    deals = [ {"title":"FaT DealS", "desc":"Breakfast buffet with copious amounts of bacon", "category":"Food",
               "price":6.99, "up":RNG.randint(1,100), "down":RNG.randint(1,33)},
              {"title":"Air Jordans", "desc":"Whaddup fams, theres some mad deals on Air Jordans right now go check em out. Don't for get to use your student discount.", "category":"Fashion",
               "price":39.99, "up":RNG.randint(1,100), "down":RNG.randint(1,33)},
              {"title":"iPhone X", "desc":"Apple Genius here, just wanted to inform you guys of the LATEST deals we have at the Apple Store, drop by to pick up your iPhone X now!!!", "category":"Electronics",
               "price":99999.99, "up":RNG.randint(1,100), "down":RNG.randint(1,33)}
              ]
    comments = [ {"userid":0, "dealid":0, "desc":"haHAA"},
                 {"userid":1, "dealid":1, "desc":"lMAO"},
                 {"userid":2, "dealid":2, "desc":"eyyyyyy"},
                 {"userid":3, "dealid":2, "desc":"goodshit"}]
    print(usernames)
    for cat_name in categories:
        add_cat(cat_name)
    for user in users:
        add_user(user["fname"].lower()+user["lname"].lower(), user["fname"], user["lname"], user["email"], user["likes"], user["auth"])
    #for deal in deals:
    #    add_deals(deal["title"], deal["desc"], categories.index(deal["category"]), usernames[0], deal["price"], deal["up"], deal["down"])
    #for comment in comments:
    #    add_comments(comment["userid"], comment["dealid"], comment["desc"])
    

def add_cat(name):
    c = Category.objects.get_or_create(name=name)[0]
    c.save()
    return c
    
def add_user(uname,fname,lname,email,likes,auth):
    u = User.objects.get_or_create(username=uname,email=email,first_name=fname,last_name=lname,
                                   likes=likes,authority=auth,password="abc")
    u.save()
    return u

def add_deals(title,desc, catid, uname, price, up, down):
    d = Deal.objects.get_or_create(category_id=catid,user_id=uname,title=title, description=desc, price=price, upvotes=up, downvotes=down)
    d.save()
    return d

def add_comments(dealid,userid,content):
    c = Comment.objects.get_or_create(deal_id=dealid, user_id=userid, content=content)
    c.save()
    return c
    
populate()