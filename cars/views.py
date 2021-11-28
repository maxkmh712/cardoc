import json, re, requests

from django.db    import transaction
from django.views import View
from django.http  import JsonResponse

from users.models import User
from users.utils  import login_decorator
from cars.models  import *


class TrimView(View):
  def post(self, request):
    try:
      with transaction.atomic():
        data = json.loads(request.body)

        if len(data) > 5:
          return JsonResponse({'message' : "TOO_MUCH_DATA"}, status = 400)

        for datum in data:
          login_id = datum["login_id"]
          trimId   = datum['trimId']
          response = requests.get(f"https://dev.mycar.cardoc.co.kr/v1/trim/{trimId}").json()
          user     = User.objects.get(login_id = login_id)

          if not User.objects.filter(login_id = login_id).exists():
            return JsonResponse({'message' : 'INVALID_LOGIN_ID'}, status = 400)


      trimName        = response['trimName']
      front_tire_info = response['spec']['driving']['frontTire']['value']
      rear_tire_info  = response['spec']['driving']['frontTire']['value']

      if not (re.compile("\d+[/]\d+R\d+").match(front_tire_info) and re.compile("\d+[/]\d+R\d+").match(rear_tire_info)):
        return JsonResponse({'message' : 'INVALID_TIRE_FORMAT'}, status = 400)
      
      front_tire_values = re.split(r'[/,R]', front_tire_info)
      rear_tire_values  = re.split(r'[/,R]', rear_tire_info)

      front_tire, _  = Tire.objects.get_or_create(
        width        = front_tire_values[0], 
        aspect_ratio = front_tire_values[1], 
        wheel_size   = front_tire_values[2]
        )
      rear_tire, _   = Tire.objects.get_or_create(
        width        = rear_tire_values[0], 
        aspect_ratio = rear_tire_values[1], 
        wheel_size   = rear_tire_values[2]
        )
      trim, _      = Trim.objects.get_or_create(
        trimName   = trimName, 
        front_tire = front_tire, 
        rear_tire  = rear_tire
        )

      UserTrim.objects.get_or_create(
        user = user, 
        trim = trim
        )

      return JsonResponse({'message' : 'SUCCESS'}, status = 201)

    except KeyError:
      return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)
    
    except User.DoesNotExist:
      return JsonResponse({'message' : "INVALID_USER_ID"}, status = 400)

  @login_decorator
  def get(self, request):
    user = request.user
    offset = int(request.GET.get('offset', 0))
    limit  = int(request.GET.get('limit', 5))
    trims  = user.trim_set.all()[offset : offset + limit]
    
    tires = [{
      'trimId'                  : trim.id,
      'trimName'                : trim.trimName,
      'front_tire' : {
        'front_tire_id'           : trim.front_tire.id,
        'front_tire_width'        : trim.front_tire.width,
        'front_tire_aspect_ratio' : trim.front_tire.aspect_ratio,
        'front_tire_wheel_size'   : trim.front_tire.wheel_size,
      },
      'rear_tire' : {
        'rear_tire_id'            : trim.rear_tire.id,
        'rear_tire_width'         : trim.rear_tire.width,
        'rear_tire_aspect_ratio'  : trim.rear_tire.aspect_ratio,
        'rear_tire_wheel_size'    : trim.rear_tire.wheel_size,
      }
    } for trim in trims]

    return JsonResponse({'message' : 'SUCCESS', 'tires' : tires}, status = 200)