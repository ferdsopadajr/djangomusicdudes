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
  path('browse/', views.browse),
  path('favorites/', views.favorites),
  path('gen_rec/', views.gen_rec),
  path('duration/', views.duration),
  path('add_to_pref/', views.add_to_pref),
  path('convert_time/', views.convert_time),
  path('upd_cbl/', views.upd_cbl),
  path('backend_process/', views.backend_process),
  path('add_to_fav/', views.add_to_fav),
  path('del_to_fav/', views.del_to_fav),
]