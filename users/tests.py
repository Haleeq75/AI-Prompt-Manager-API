from urllib import response
from django.test import TestCase


from rest_framework.response import Response
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from django.urls import reverse


# Create your tests here.
class AuthenticateTest(APITestCase):
    def setUp(self):
        self.username = 'testuser'
        self.email = 'testuser@example.com'
        self.password = 'testpassword123'
        self.user= User.objects.create_user(
            username=self.username,
            email=self.email, 
            password=self.password)
        
        
        self.register_url = reverse('register')
        self.login_url = reverse('login')   
        self.test_auth_url = reverse('test_auth')
        
    
    #------------------------Normal Cases------------------------
    
    # Normal case: Test user registration, login, and access to protected view    
    def test_registration(self):
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpassword123'
        }
        response = self.client.post(self.register_url, data, format='json')
        #check if the response status code is 201 (created)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        #check if the user was created in the database
        self.assertTrue(User.objects.filter(username=data['username']).exists())
        
    def test_login(self):
        data = {
            'username': self.username,
            'password': self.password
        }
        response = self.client.post(self.login_url, data, format='json')
        #check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        #verify that the response contains access and refresh tokens
        self.assertIn('access', response.data)# type: ignore
        self.assertIn('refresh', response.data)# type: ignore
        
    def test_protected_view(self):
        #1.test without authentication
        response= self.client.get(self.test_auth_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        #2.test with authentication
        login_data =self.client.post(self.login_url, {
            'username': self.username, 
            'password': self.password
            },format='json')
        access_token = login_data.data['access']# type: ignore
        # Attach token to the header (just like Postman 'Bearer')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)# type: ignore
        
        response = self.client.get(self.test_auth_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user'], self.username)# type: ignore
        
    def test_token_refresh(self):
        # First, log in to get the refresh token
        login_data = self.client.post(self.login_url, {
            'username': self.username,
            'password': self.password
        }, format='json')
        refresh_token = login_data.data['refresh']# type: ignore
        
        # Now, test the token refresh endpoint
        response = self.client.post(reverse('token_refresh'), {
            'refresh': refresh_token
        }, format='json')
        
        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Verify that the response contains a new access token
        self.assertIn('access', response.data) # type: ignore
        
    #------------------------Edge Cases------------------------
    
    # Edge case: Login based Authentication Failures 
      
    def test_register_duplicate_username(self):
        # Data for a user that already exists (created in setUp)
        data = {
            'username': self.username, # 'testuser' already exists
            'email': 'different@example.com',
            'password': 'newpassword123'
        }
        response = self.client.post(self.register_url, data, format='json')

        # Assert that it fails with 400
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Check if the error message mentions the username
        self.assertIn('username', response.data)# type: ignore
        
    def test_register_duplicate_email(self):
        # Data for a user with an email that already exists (created in setUp)
        data = {
            'username': 'differentuser',
            'email': self.email, # 'testuser@example.com' already exists
            'password': 'newpassword123'
        }
        response = self.client.post(self.register_url, data, format='json')

        # Assert that it fails with 400
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Check if the error message mentions the email
        self.assertIn('email', response.data)# type: ignore
    
    # Edge case: Token Based Authentication Failures
    
    def test_tampered_token(self):
        # Log in to get a valid access token
        login_data = self.client.post(self.login_url, {
            'username': self.username,
            'password': self.password
        }, format='json')
        access_token = login_data.data['access']# type: ignore
        
        # Tamper with the token (e.g., change a character)
        tampered_token = access_token[:-1] + ('a' if access_token[-1] != 'a' else 'b')
        
        # Attach the tampered token to the header
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + tampered_token)# type: ignore
        
        # Attempt to access the protected view
        response = self.client.get(self.test_auth_url)
        
        # Assert that it fails with 401 Unauthorized
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['code'], 'token_not_valid')# type: ignore
        
    def test_malformed_token(self):
        # Attach a completely malformed token to the header
        self.client.credentials(HTTP_AUTHORIZATION='Bearer malformedtoken123')# type: ignore
        
        # Attempt to access the protected view
        response = self.client.get(self.test_auth_url)
        
        # Assert that it fails with 401 Unauthorized
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['code'], 'token_not_valid')# type: ignore
    
    def test_missing_token(self):
        # Ensure no token is attached to the header
        self.client.credentials()#type: ignore
        # Attempt to access the protected view
        response = self.client.get(self.test_auth_url) 
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')# type: ignore
        
    def test_refresh_with_invalid_token(self):
        # First, log in to get a valid refresh token
        login=self.client.post(self.login_url, {
            'username': self.username,
            'password': self.password
        }, format='json')   
        access_token = login.data['access']# type: ignore
        
        #Using access token instead of refresh token to test refresh endpoint
        refresh_url = reverse('token_refresh')
        response = self.client.post(refresh_url, {
            'refresh': access_token
        }, format='json')
        
        #It should fail with 401 Unauthorized because access token is not valid for refresh
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)        
        