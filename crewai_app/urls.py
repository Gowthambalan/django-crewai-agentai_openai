from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),  # for web form UI
    path("api/query/", views.api_query, name="api_query"),  # for Postman JSON API
]
