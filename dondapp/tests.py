import datetime
import pytz
from django.db.models import Q

from dondapp import models

from django.test import TestCase


# Create your tests here.
class BaseTestCases:
    class ResourceTestCase(TestCase):
        @classmethod
        def setUpClass(cls):
            super().setUpClass()

        def test_get(self):
            response = self.client.get(self.path)
            self.assertEqual(response.status_code, 405, 'Should not support GET method')

        def test_post(self):
            response = self.client.post(self.path)
            self.assertEqual(response.status_code, 405, 'Should not support POST method')

        def test_head(self):
            response = self.client.head(self.path)
            self.assertEqual(response.status_code, 405, 'Should not support HEAD method')

        def test_put(self):
            response = self.client.put(self.path)
            self.assertEqual(response.status_code, 405, 'Should not support PUT method')

        def test_delete(self):
            response = self.client.delete(self.path)
            self.assertEqual(response.status_code, 405, 'Should not support DELETE method')

        def test_options(self):
            response = self.client.options(self.path)
            self.assertEqual(response.status_code, 405, 'Should not support OPTIONS method')

        def test_trace(self):
            response = self.client.trace(self.path)
            self.assertEqual(response.status_code, 405, 'Should not support TRACE method')


class HomeViewTest(BaseTestCases.ResourceTestCase):
    path = '/'

    def test_get(self):
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, 200, 'Home should return OK on GET request')
        self.assertEqual(len(response.templates), 2, 'Home should only use index and base templates')


class AboutView(BaseTestCases.ResourceTestCase):
    path = '/about/'

    def test_get(self):
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, 200, 'About should return OK on GET request')
        self.assertEqual(len(response.templates), 2, 'About should only use about and base templates')


class FailedView(BaseTestCases.ResourceTestCase):
    path = '/about/'

    def test_get(self):
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, 200, 'Failed should return OK on GET request')


class SearchView(BaseTestCases.ResourceTestCase):
    path = '/search/'

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        user = models.User.objects.create_user("johnsmith", "John", "Smith", "john@smith.com", "abcdefghi123")
        category = models.Category.objects.create(name="Food", description="Food based deals")
        models.Deal.objects.create(category_id=category, user_id=user, title="McDonalds Deal",
                                   description="Free Cheeseburger with saver meal", price=0.0)
        models.Deal.objects.create(category_id=category, user_id=user, title="KFC",
                                   description="Free Wing with saver meal", price=0.0)

    def test_get_empty(self):
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, 400, 'Search should produce BadRequest when no query given')

    def test_get(self):
        response = self.client.get(self.path, data={'query': 'burger'})
        self.assertContains(response, 'Free Cheeseburger with saver meal', status_code=200)

    def test_get_none(self):
        response = self.client.get(self.path, data={'query': 'hotdog'})
        self.assertNotContains(response, 'Free Cheeseburger with saver meal', status_code=200)
        self.assertNotContains(response, 'Free Wing with saver meal', status_code=200)

    def test_get_both(self):
        response = self.client.get(self.path, data={'query': 'Free'})
        self.assertContains(response, 'Free Cheeseburger with saver meal', status_code=200)
        self.assertContains(response, 'Free Wing with saver meal', status_code=200)

    @classmethod
    def tearDownClass(cls):
        for deal in models.Deal.objects.filter(Q(title__contains='McDonalds') | Q(title__contains='KFC')):
            deal.delete()
        for category in models.Category.objects.filter(name='Food'):
            category.delete()
        for user in models.User.objects.filter(username='johnsmith'):
            user.delete()
        super().tearDownClass()


class DealViewTest(BaseTestCases.ResourceTestCase):
    path = '/deal/'

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        user = models.User.objects.create_user("johnsmith", "John", "Smith", "john@smith.com", "abcdefghi123")
        user2 = models.User.objects.create_user("joeblogs", "Joe", "Blogs", "joe@blogs.com", "abcdefghi123")
        category = models.Category.objects.create(name="Food", description="Food based deals")
        mc_deal = models.Deal.objects.create(category_id=category, user_id=user, title="McDonalds Deal",
                                             description="Free Cheeseburger with saver meal", price=0.0)
        kfc_deal = models.Deal.objects.create(category_id=category, user_id=user2, title="KFC",
                                              description="Free Wing with saver meal", price=0.0)
        mc_deal.upvoters.set([user])
        mc_deal.downvoters.set([user2])
        kfc_deal.upvoters.set([user, user2])

    @classmethod
    def tearDownClass(cls):
        for deal in models.Deal.objects.filter(Q(title='McDonalds Deal') | Q(title='KFC')):
            deal.delete()
        for category in models.Category.objects.filter(name='Food'):
            category.delete()
        for user in models.User.objects.filter(Q(username='johnsmith') | Q(username='joeblogs')):
            user.delete()
        super().tearDownClass()

    def test_get_empty(self):
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, 404)

    def test_get(self):
        response = self.client.get(self.path + '1/')
        self.assertContains(response, 'Free Cheeseburger')

    def test_post(self):
        response = self.client.post(self.path, data={
            'category_id': models.Category.objects.all()[0].id,
            'user_id': 'johnsmith',
            'title': 'New Deal',
            'description': 'New Deal',
            'price': 0.0
        })
        self.assertEqual(response.status_code, 200, response.content)
        self.assertEqual(len(models.Deal.objects.filter(title='New Deal')), 1, 'Failed to create deal')
        for deal in models.Deal.objects.filter(title='New Deal'):
            deal.delete()

    def test_post_missing(self):
        response = self.client.post(self.path, data={
            'category_id': models.Category.objects.all()[0].id,
            'user_id': 'johnsmith',
            'title': 'New Deal',
            'price': 0.0
        })
        self.assertEqual(response.status_code, 400, 'Should fail when given incomplete deal')

    def test_post_not_found(self):
        response = self.client.post(self.path, data={
            'category_id': 999,
            'user_id': 'johnsmith',
            'title': 'New Deal',
            'description': 'New Deal',
            'price': 0.0
        })
        self.assertEqual(response.status_code, 404, 'Should fail when given invalid category')

        response = self.client.post(self.path, data={
            'category_id': models.Category.objects.all()[0].id,
            'user_id': 'NOT REAL USER NAME',
            'title': 'New Deal',
            'description': 'New Deal',
            'price': 0.0
        })
        self.assertEqual(response.status_code, 404, 'Should fail when given invalid user')


class NewDealViewTest(BaseTestCases.ResourceTestCase):
    path = '/newdeals/'

    def test_get(self):
        response = self.client.get(self.path)
        json = response.json()
        self.assertEqual(json, sorted(json, key=lambda x: x["creation_date"]))


class TopDealViewTest(BaseTestCases.ResourceTestCase):
    path = '/topdeals/'

    def test_get(self):
        response = self.client.get(self.path)
        json = response.json()
        self.assertEqual(json, sorted(json, key=lambda x: x["upvotes"], reverse=True))


class CommentViewTest(BaseTestCases.ResourceTestCase):
    path = '/comment/'

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        user = models.User.objects.create_user("johnsmith", "John", "Smith", "john@smith.com", "abcdefghi123")
        user2 = models.User.objects.create_user("joeblogs", "Joe", "Blogs", "joe@blogs.com", "abcdefghi123")
        category = models.Category.objects.create(name="Food", description="Food based deals")
        mc_deal = models.Deal.objects.create(category_id=category, user_id=user, title="McDonalds Deal",
                                             description="Free Cheeseburger with saver meal", price=0.0)
        models.Comment.objects.create(deal_id=mc_deal, user_id=user, content='Quality Deal M8',
                                      creation_date=pytz.utc.localize(datetime.datetime.now()))
        models.Comment.objects.create(deal_id=mc_deal, user_id=user2, content='Quality Deal M8',
                                      creation_date=pytz.utc.localize(datetime.datetime.now()))

    @classmethod
    def tearDownClass(cls):
        for comment in models.Comment.objects.filter(content__contains='M8'):
            comment.delete()
        for deal in models.Deal.objects.filter(title='McDonalds Deal'):
            deal.delete()
        for category in models.Category.objects.filter(name='Food'):
            category.delete()
        for user in models.User.objects.filter(Q(username='johnsmith') | Q(username='joeblogs')):
            user.delete()
        super().tearDownClass()

    def test_get_none(self):
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, 400, 'Should fail if not given comment id')

    def test_get(self):
        response = self.client.get(self.path, data={'id': 1})
        json = response.json()
        self.assertEqual(json['deal_id'], 1)
        self.assertEqual(json['user_id'], 'johnsmith')
        self.assertEqual(json['content'], 'Quality Deal M8')

    def test_post_unauth(self):
        response = self.client.post(self.path)
        self.assertEqual(response.status_code, 401, "Unauthorised user shouldn't be able to comment")

    def test_post(self):
        self.client.login(username='johnsmith', password='abcdefghi123')
        comment_data = {
            'deal_id': 1,
            'user_id': 'joeblogs',
            'creation_date': str(pytz.utc.localize(datetime.datetime.now())),
            'content': 'CONTENT GOES HERE'
        }
        response = self.client.post(self.path, data=comment_data)
        self.assertEqual(response.status_code, 200)
        comment = models.Comment.objects.filter(content='CONTENT GOES HERE')
        self.assertTrue(comment is not None)
        comment.delete()
        self.client.logout()

    def test_delete_unauth(self):
        response = self.client.delete(self.path + '1/')
        self.assertEqual(response.status_code, 401, 'Unauthorised users should not be able to delete comments')

    def test_delete(self):
        comment = models.Comment.objects.create(deal_id=models.Deal.objects.get(id=1),
                                                user_id=models.User.objects.get(username='joeblogs'),
                                                content='Best dealo', creation_date=pytz.utc.localize(datetime.datetime.now()))
        self.client.login(username='joeblogs', password='abcdefghi123')
        response = self.client.delete(self.path + str(comment.id) + '/')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(models.Comment.objects.filter(content='Best dealo').exists())
        self.client.logout()

    def test_delete_forbid(self):
        comment = models.Comment.objects.create(deal_id=models.Deal.objects.get(id=1),
                                                user_id=models.User.objects.get(username='johnsmith'),
                                                content='Best dealo', creation_date=pytz.utc.localize(datetime.datetime.now()))
        self.client.login(username='joeblogs', password='abcdefghi123')
        response = self.client.delete(self.path + str(comment.id) + '/')
        self.assertEqual(response.status_code, 403)
        comment.delete()
        self.client.logout()


class UserView(BaseTestCases.ResourceTestCase):
    path = '/user/'

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        models.User.objects.create_user("johnsmith", "John", "Smith", "john@smith.com", "abcdefghi123")
        models.User.objects.create_user("joeblogs", "Joe", "Blogs", "joe@blogs.com", "abcdefghi123")

    @classmethod
    def tearDownClass(cls):
        for user in models.User.objects.filter(Q(username='johnsmith') | Q(username='joeblogs')):
            user.delete()
        super().tearDownClass()

    def get_profile(self):
        response = self.client.get(self.path + 'johnsmith/')
        self.assertContains(response, 'john@smith.com', 'Profile page should show the email of a user')
        self.assertNotContains(response, 'abcdefghi123', ' Profile page should not show passwords')

    def get_fake_profile(self):
        response = self.client.get(self.path + 'NOTREAL/')
        self.assertEqual(response.status_code, 404, 'Should fail to find user')

    def get_none(self):
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, 404, 'Should fail to find user')

    def get_fake(self):
        response = self.client.get(self.path, data={'username': 'NOTREAL'})
        self.assertEqual(response.status_code, 404, 'Should fail to find user')

    def get(self):
        response = self.client.get(self.path, data={'username': 'johnsmith'})
        json = response.json()
        self.assertEqual(json['email'], 'john@smith.com', 'Failed to get correct user json')
        self.assertTrue('password' not in json)
