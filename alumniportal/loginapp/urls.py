from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.signup_view, name="signup"),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('', views.home_view, name="home"),
    path('changepass/', views.changepass_view, name="cpass")
]
