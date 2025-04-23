from django.urls import path
from . import views

urlpatterns = [
    path('', views.root_redirect),  # Redirige / a /login/
    path('login/', views.login_view, name='login'),
]
