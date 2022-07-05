from django.urls import path
from . import views

urlpatterns = [
    path('accounts/', views.AccountsView.as_view()),
    path('accounts/newest/<int:num>/', views.AccountsNewestView.as_view()),
    path('login/', views.LoginView.as_view()),
]