from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
	path('account/', views.account),
	path('signup/', views.signup),
  path('login/', auth_views.LoginView.as_view(redirect_authenticated_user=True, template_name='overallsystem/login.html')),
  path('logout/', auth_views.LogoutView.as_view()),
  path('', views.main),
  path('main/', views.main),
  path('gen_rec/', views.gen_rec),
]