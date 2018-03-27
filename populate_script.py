# coding=utf-8
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'deal_or_no_deal.settings')
import django
django.setup()
from dondapp.models import *
import random as RNG
from django.utils import timezone


def populate():
    categories = ["Food", "Fashion", "Travel", "Electronics", "Accommodation",
                  "Health and Fitness"]
    users = [{"fname": "Jason", "lname": "Smith", "email": "jsmith@mail.com",
              "likes": RNG.randint(1, 50), "auth": 1},
             {"fname": "Jimmy", "lname": "Singer", "email": "jsinger@mail.com",
              "likes": RNG.randint(1, 50), "auth": 0},
             {"fname": "Liza", "lname": "Harpoon", "email": "lharpoon@mail.com",
              "likes": RNG.randint(1, 50), "auth": 0},
             {"fname": "Mike", "lname": "Jimson", "email": "mjimson@mail.com",
              "likes": RNG.randint(1, 50), "auth": 0},
             {"fname": "John", "lname": "Smith", "email": "bigJsmith@mail.com",
              "likes": RNG.randint(1, 50), "auth": 0}
             ]
    usernames = [users[x]["fname"].lower() + users[x]["lname"].lower() for x in range(len(users))]
    deals = [{"title": "FaT DealS", "desc": "Breakfast buffet with copious amounts of bacon", "category": "Food",
              "price": 6.99, "up": RNG.randint(1, 100), "down": RNG.randint(1, 33)},
             {"title": "Air Jordans",
              "desc": "Whaddup fams, theres some mad deals on Air Jordans right now go check em out. Don't for get to use your student discount.",
              "category": "Fashion",
              "price": 39.99, "up": RNG.randint(1, 100), "down": RNG.randint(1, 33)},
             {"title": "iPhone X",
              "desc": "Apple Genius here, just wanted to inform you guys of the LATEST deals we have at the Apple Store, drop by to pick up your iPhone X now!!!",
              "category": "Electronics",
              "price": 99999.99, "up": RNG.randint(1, 100), "down": RNG.randint(1, 33)},
             {"title": "Holiday bookings", "desc":"Don't you ever want to escape from the daily 9 to 5? Well, me too. Let's all go visit Thailand!", "category":"Travel",
              "price": 649.99, "up":RNG.randint(1000,999999), "down":0},
             {"title": "Flatmate Wanted", "desc":"Hello guys I am single ready to mingle haHAA, but no really, I am looking to rent with people. Hello? Are you still reading this? Are you guys interested? pls respond ", "category":"Accommodation",
              "price": 350, "up":RNG.randint(5,100), "down":RNG.randint(5,100)},
             {"title": "What did you just say?", "desc": "คุณตระหนักถึงสิ่งที่คุณเพิ่งพูดกะฉันคุณยกได้หรือไม่ฉันจะมีคุณรู้ว่าฉันเสร็จสิ้นด้านบนของห้องยิมของฉันในการนั่งและฉันได้มีส่วนร่วมในเน็กลับหลายม็อดและฉันมีต้นไม้สาวบาทแล้วมันตีฉันฉันเป็น ยักษ์ ฉันได้รับการฝึกฝนในมิรินและฉันเป็นอัลฟาบนสุดในโลกใบนีคุณไม่มีอะไรให้ฉัน แต่เพียงเบต้าอื่น ฉันจะเช็ดเจ้าออกมาฉันมีแขนยาว " + "18 นิ้วตัดเหมือนเพชรทำเครื่องหมายคำพูดของฉัน คุณคิดว่าคุณสามารถหนีไปได้โดยบอกว่าอึกับฉันผ่านทางอินเทอร์เน็ต? คิดอีกครั้ง, เกรียน ขณะที่เราพูดฉันกระโดดบัญชี ม็อด ของฉันและ ไอพี ของคุณจะถูกตรวจสอบในขณะนี้เพื่อให้คุณดีขึ้นเตรียมความพร้อมสำหรับพายุ หนอนชาเขียว พายุที่กวาดล้างสิ่งเล็กน้อยที่น่าสงสารที่คุณเรียกหาตัวแทนของคุณ คุณกำลังจะตาย " + "สัส ฉันสามารถไปได้ทุกที่ทุกเวลาและฉันสามารถช่วยคุณให้ได้ชุดที่สะอาดกว่า 10"+ "ในเจ็ดร้อยวิธีและนั่นเป็นเพียงแค่ใช้มือเปล่าเท่านั้น ฉันไม่เพียง แต่ได้รับการฝึกอบรมอย่างกว้างขวางใน", "category":"Health and Fitness",
              "price": 420, "up":RNG.randint(5,100), "down":RNG.randint(5,100)},
             ]
    comments = [{"userid": RNG.randint(1, len(users)-1), "dealid": RNG.randint(1, len(deals)), "desc": "haHAA"},
                {"userid": RNG.randint(1, len(users)-1), "dealid": RNG.randint(1, len(deals)), "desc": "lMAO"},
                {"userid": RNG.randint(1, len(users)-1), "dealid": RNG.randint(1, len(deals)), "desc": "eyyyyyy"},
                {"userid": RNG.randint(1, len(users)-1), "dealid": RNG.randint(1, len(deals)), "desc": "good stuff"},
                {"userid": RNG.randint(1, len(users)-1), "dealid": RNG.randint(1, len(deals)), "desc": "w0w"},
                {"userid": RNG.randint(1, len(users)-1), "dealid": RNG.randint(1, len(deals)), "desc": "u find good deal"},
                {"userid": RNG.randint(1, len(users)-1), "dealid": RNG.randint(1, len(deals)), "desc": "can u pm me some mcdonald's coupons?"},
                {"userid": 1-1, "dealid": 4, "desc": "My Dad went to buy cigarettes in Thailand... it's been 5 years. I hope he found his Marlboros"},
                {"userid": 5-1, "dealid": 4, "desc": "s-son? is that you? i found the Marlboro Ice Blast, im on my way home son."},
                {"userid": 3-1, "dealid": 4, "desc": "WAIT WHAT?! ^"},
                {"userid": 1-1, "dealid": 6, "desc": "what did he mean by this?"},
                {"userid": 2-1, "dealid": 6, "desc": "?"},
                ]
    # print(usernames)
    for cat_name in categories:
        add_cat(cat_name)
    for user in users:
        add_user(user["fname"].lower() + user["lname"].lower(), user["fname"], user["lname"], user["email"],
                 user["likes"], user["auth"])
    # print(Category.objects.get(name="Food"))
    # print(timezone.now())
    for deal in deals:
        add_deals(deal["title"], deal["desc"], Category.objects.get(name=deal["category"]),
                  User.objects.all()[RNG.randint(1,len(users)-1)], deal["price"], deal["up"], deal["down"])
    for comment in comments:
        #print(comment["userid"], comment["dealid"])
        add_comments(User.objects.get(username=usernames[comment["userid"]]), Deal.objects.get(id=comment["dealid"]), comment["desc"])


def add_cat(name):
    c = Category.objects.get_or_create(name=name)[0]
    c.save()
    return c


def add_user(uname, fname, lname, email, likes, auth):
    u = User.objects.create_user(username=uname, email=email, first_name=fname, last_name=lname,
                                 likes=likes, authority=auth, password="abcdefghijkl")
    u.save()
    return u


def add_deals(title, desc, catid, uname, price, up, down):
    d = Deal.objects.get_or_create(category_id=catid, user_id=uname, title=title, description=desc, price=price, upvotes=up,
                               downvotes=down, creation_date=timezone.now())[0]
    d.save()
    return d


def add_comments(userid, dealid, content):
    c = Comment.objects.get_or_create(deal_id=dealid, user_id=userid, content=content, creation_date=timezone.now())[0]
    c.save()
    return c


populate()
