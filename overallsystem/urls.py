from django.urls import path
from . import views

urlpatterns = [
  path('login/', views.login),
	path('', views.main),
  path('main/', views.main),
]