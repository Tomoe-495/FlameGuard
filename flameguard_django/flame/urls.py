from django.urls import path
from .views import home, get_prediction

urlpatterns = [
    path('', home, name='home'),
    path('prediction', get_prediction, name='prediction')
]