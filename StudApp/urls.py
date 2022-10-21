from django.urls import path
from django.conf.urls import include
from .views import *
from . import views


app_name = 'StudApp'

urlpatterns = [
    path('login/',LoginApi.as_view(), name='LoginApi'),
    # path('add_user/',UserAddApi.as_view(), name='UserAddApi'),
    path('register/', RegisterAPI.as_view(), name='RegisterAPI'),
    path('signup/', RegisterUser.as_view(), name='RegisterUser'),
    path('search/',SearchListAPI.as_view(), name='SearchListAPI'),
    path('', StudentsListAPI.as_view(), name="StudentsListAPI"),
   # path('', StudentsListAPI.as_view(), name="StudentsListAPI"),
    path('studentsapi/<int:pk>/', StudentApi.as_view(), name="StudentApi"),
    # path('ratingapi/', RatingListAPI.as_view(), name="RatingListAPI"),
    # path('ratingapi/<int:pk>/', RateApi.as_view(), name="RateApi"),

]



