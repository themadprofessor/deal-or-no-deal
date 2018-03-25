from dondapp import models
from django.test import TestCase


# Create your tests here.
class BaseTestCases:
    class ResourceTestCase(TestCase):
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

    def setUp(self):
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

