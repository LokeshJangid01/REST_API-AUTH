from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token

class ViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpassword'
        }
        self.user = User.objects.create_user(**self.user_data)
        self.token = Token.objects.create(user=self.user)

    def test_login(self):
        response = self.client.post('http://localhost:8000/login/',self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token',response.data)
        self.assertIn('user',response.data)

    def test_login_invalid_credentials(self):
        invalid_data = {
            'username': 'LokiTheGod1',
            'password': 'Pass1234!'
        }
        response = self.client.post('http://localhost:8000/login/',invalid_data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    def test_signup(self):
        new_user_data = {
            'username':'LokiTheGod2',
            'password':'Pass1234!',
            'email':'loki2@thegod.com'
        }
        response = self.client.post('http://localhost:8000/signup/',new_user_data)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertIn('token',response.data)
        self.assertIn('user',response.data)
    
    def test_test_token(self):
        #token = Token.objects.create(user = self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.get('http://localhost:8000/test-token/')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data,f"Passed for, {self.user.email}")






