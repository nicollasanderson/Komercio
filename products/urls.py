from django.urls import path, include
from . import views

urlpatterns = [
    path('products/', views.CreateListProductsView.as_view()),
    path('products/<int:pk>/', views.UpdateListOneProductView.as_view()),
]