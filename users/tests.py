import json, jwt, bcrypt
from os import access
from django.http import response

from django.test import TestCase, Client, client

from cardoc.settings import SECRET_KEY, ALGORITHM
from users.models import User

class SignUpTest(TestCase):
  def setUp(self):
    user = User.objects.create(
      id = 1,
      login_id = 'user1',
      password = bcrypt.hashpw('111111'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
      )

  def tearDown(self):
    User.objects.all().delete()

  def test_sign_up_post_success(self):
    client = Client()
    data   = {
      'login_id' : 'user2',
      'password' : '222222'
    }
    response = client.post('/users/signup', json.dumps(data), content_type = 'application/json')

    self.assertEqual(response.json(),{'message' : 'SUCCESS'})
    self.assertEqual(response.status_code, 200)

  def test_sign_up_failure_login_id_already_exists(self):
    client = Client()
    data   = {
      'login_id' : 'user1',
      'password' : '111111'
    }
    response = client.post('/users/signup', json.dumps(data), content_type = 'application/json')

    self.assertEqual(response.json(),{'message' : 'LOGIN_ID_ALREADY_EXISTS'})
    self.assertEqual(response.status_code, 400)

  def test_sign_up_failure_key_error(self):
    client = Client()
    data   = {
      
      'password' : '222222'
    }
    response = client.post('/users/signup', json.dumps(data), content_type = 'application/json')

    self.assertEqual(response.json(),{'message' : 'KEY_ERROR'})
    self.assertEqual(response.status_code, 400)

class SignInTest(TestCase):
  def setUp(self):
    user = User.objects.create(
      id       = 1,
      login_id = 'user1',
      password = bcrypt.hashpw('111111'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
      )
    global access_token
    access_token = jwt.encode({'login_id':user.login_id}, SECRET_KEY, ALGORITHM)

  def tearDown(self):
    User.objects.all().delete()

  def test_sign_in_post_success(self):
    client = Client()
    data = {
      'login_id' : 'user1',
      'password' : '111111'
    }
    response = client.post('/users/signin', json.dumps(data), content_type = 'application/json')

    self.assertEqual(response.json(),{'access_token' : access_token})
    self.assertEqual(response.status_code, 200)

  def test_sign_in_failure_invalid_login_id(self):
    client = Client()
    data = {
      'login_id' : 'wronguser',
      'password' : '111111'
    }
    response = client.post('/users/signin', json.dumps(data), content_type = 'application/json')

    self.assertEqual(response.json(),{'message' : 'INVALID_LOGIN_ID'})
    self.assertEqual(response.status_code, 401)

  def test_sign_in_failure_invalid_password(self):
    client = Client()
    data = {
      'login_id' : 'user1',
      'password' : '222222'
    }
    response = client.post('/users/signin', json.dumps(data), content_type = 'application/json')

    self.assertEqual(response.json(),{'message' : 'INVALID_PASSWORD'})
    self.assertEqual(response.status_code, 401)

  def test_sign_in_failure_key_error(self):
    client = Client()
    data = {

      'password' : '222222'
    }
    response = client.post('/users/signin', json.dumps(data), content_type = 'application/json')

    self.assertEqual(response.json(),{'message' : 'KEY_ERROR'})
    self.assertEqual(response.status_code, 400)