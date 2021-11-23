import json, bcrypt, jwt

from django.http  import JsonResponse
from django.views import View

from users.models import User
from my_settings  import SECRET_KEY, ALGORITHM

class SignUpView(View):
  def post(self, request):
    data = json.loads(request.body)

    login_id = data['login_id']
    password = data['password']
    name     = data.get('name')

    try:
      if User.objects.filter(login_id = login_id).exists():
        return JsonResponse({'message' : 'LOGIN_ID_ALREADY_EXISTS'}, status = 400)

      hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
      decoded_pw = hashed_pw.decode('utf-8')

      User.objects.create(
        login_id = login_id,
        password = decoded_pw,
        name     = name
      )

      return JsonResponse({'message' : 'SUCCESS'}, status = 200)
    
    except KeyError:
      return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)

class SignInView(View):
  def post(self, request):
    try:
      data = json.loads(request.body)

      login_id = data['login_id']
      password = data['password']

      if not (login_id and password):
        return JsonResponse({'message' : 'EMPTY_VALUE'}, status = 400)

      if not User.objects.filter(login_id = login_id).exists():
        return JsonResponse({'message' : 'INVALID_EMAIL'}, status = 401)

      user = User.objects.get(login_id = login_id)

      if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        return JsonResponse({'message' : 'INVALID_PASSWORD'}, status = 401)

      access_token = jwt.encode({'login_id' : user.login_id}, SECRET_KEY, ALGORITHM)
      return JsonResponse({'access_token' : access_token}, status = 200)

    except KeyError:
      return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)

    except ValueError:
      return JsonResponse({'message' : 'VALUE_ERROR'}, status = 400)