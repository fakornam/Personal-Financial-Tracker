from django.urls import path
from .views import (
    home_view,
    RegisterView,
    LoginView,
    TransactionListCreateView,
    TransactionDetailView,
    CategoryListCreateView
)

urlpatterns = [
    path('', home_view, name='home'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('transactions/', TransactionListCreateView.as_view(), name='transactions'),
    path('transactions/<int:pk>/', TransactionDetailView.as_view(), name='transaction-detail'),
    path('categories/', CategoryListCreateView.as_view(), name='categories'),
]