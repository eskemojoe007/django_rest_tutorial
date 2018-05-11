# from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory
from rest_framework.test import APIClient
from . import apiviews
from django.contrib.auth import get_user_model
from django.urls import reverse
# Create your tests here.
class TestPoll(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.factory = APIRequestFactory()
        self.view = apiviews.PollViewSet.as_view({'get':'list'})
        self.uri = reverse('polls:polls-list')
        self.user = self.setup_user()

    @staticmethod
    def setup_user():
        User = get_user_model()
        return User.objects.create_user(
            'test',
            email='test@test.com',
            password='test_pass'
        )

    def test_list(self):
        request = self.factory.get(self.uri)
        request.user = self.user
        response = self.view(request)
        self.assertEqual(
            response.status_code,200,
            'Expected Response code 200, recieved {} instead.'
            .format(response.status_code))

    def test_list2(self):
        self.client.login(username='test',password='test_pass')
        response = self.client.get(self.uri)
        self.assertEqual(
            response.status_code,200,
            'Expected Response code 200, recieved {} instead.'
            .format(response.status_code))
    def test_create(self):
        self.client.login(username='test',password='test_pass')
        params = {
            'question':'Test question?',
            'created_by':1
        }

        response = self.client.post(self.uri,params)
        self.assertEqual(
            response.status_code,201,
            'Expected Response code 201, recieved {} instead.'
            .format(response.status_code))
