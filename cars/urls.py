from django.urls import path

from cars.views import TrimView

urlpatterns = [
  path('', TrimView.as_view())
]