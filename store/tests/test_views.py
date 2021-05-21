from pprint import pprint

from django.contrib.auth.models import User
from django.http import HttpRequest
# from unittest import skip
from django.test import Client, RequestFactory, TestCase
from django.urls import reverse

from store.models import Category, Product
from store.views import product_all


#
# @skip('demonstrating skipping')
# class TestSkip(TestCase):
#     def test_skip_example(self):
#         pass
#
class TestViewResponses(TestCase):
    def setUp(self) -> None:
        self.c = Client()
        self.factory = RequestFactory()
        User.objects.create(username='admin')
        Category.objects.create(name='java', slug='java')
        Product.objects.create(category_id=1, title='java beginners', created_by_id=1,
                               slug='java-beginners', price=20.00, image='java')

    def test_url_allowed_hosts(self):
        response = self.c.get('/')
        self.assertEqual(response.status_code, 200)

    def test_product_detail_url(self):
        response = self.c.get(reverse('store:product_detail', args=['java-beginners']))
        self.assertEqual(response.status_code, 200)

    def test_category_detail_url(self):
        response = self.c.get(reverse('store:category_list', args=['java']))
        self.assertEqual(response.status_code, 200)

    def test_homepage_html(self):
        request = HttpRequest()
        response = product_all(request)
        html = response.content.decode('utf8')
        pprint(html)
        self.assertIn('<title>Home</title>', html)
        self.assertTrue(html.startswith('\n<!DOCTYPE html>\n'))

    def test_view_function(self):
        request = self.factory.get('/item/java-beginners')
        response = product_all(request)
        html = response.content.decode('utf8')
        self.assertIn('<title>Home</title>', html)
        self.assertTrue(html.startswith('\n<!DOCTYPE html>\n'))
        self.assertEqual(response.status_code, 200)
