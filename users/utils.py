import jwt

from django.http import JsonResponse

from my_settings import SECRET_KEY, ALGORITHM
from users.models import User

def login_decorator(func):
  def wrapper(self, request, *args, **kwargs):
    try:
      access_token = request.headers.get('Authorization')
      payload      = jwt.decode(access_token, SECRET_KEY, ALGORITHM)
      user         = User.objects.get(login_id = payload['login_id'])
      request.user = user

    except jwt.exceptions.DecodeError:
      return JsonResponse({'message' : 'INVALID_TOKEN'}, status = 400)

    except User.DoesNotExist:
      return JsonResponse({'message' : 'INVALID_USER'}, status = 400)

    return func(self, request, *args, **kwargs)

  return wrapper
