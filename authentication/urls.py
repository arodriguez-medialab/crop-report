from django.urls import path
from authentication import views

urlpatterns = [
  path('login/', views.login_view, name = 'login'),
  path('home/', views.home, name = 'home'),
  path('signin/', views.sign_in, name = 'signin'),
  path('admin_signin/', views.admin_sign_in, name = 'admin_signin'),
  path('callback/', views.callback, name = 'callback'),
  path('signout/', views.sign_out, name = 'signout'),
]
