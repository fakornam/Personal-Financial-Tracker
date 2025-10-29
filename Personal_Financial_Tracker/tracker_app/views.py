import requests
from rest_framework import generics, permissions
from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.shortcuts import redirect
from .models import Transaction, Category
from .serializers import (
    RegisterSerializer,
    TransactionSerializer,
    CategorySerializer
)

User = get_user_model()

# Home page
def home_view(request):
    return render(request, 'home.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        response = requests.post('http://127.0.0.1:8000/auth/login/', json={
            'username': username,
            'password': password
        })

        if response.status_code == 200:
            token = response.json()['access']
            request.session['access_token'] = token
            return redirect('dashboard')
        else:
            return render(request, 'login_form.html', {'error': 'Invalid credentials'})

    return render(request, 'login_form.html')


def dashboard_view(request):
    token = request.session.get('access_token')
    if not token:
        return redirect('login')

    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get('http://127.0.0.1:8000/transactions/', headers=headers)

    transactions = response.json() if response.status_code == 200 else []
    return render(request, 'dashboard.html', {'transactions': transactions})

# Register
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

# Logout page (browser-friendly)
@method_decorator(csrf_exempt, name='dispatch')
class LogoutPageView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return render(request, 'logout.html')

    def post(self, request):
        return render(request, 'logout_success.html')

# Transactions
class TransactionListCreateView(generics.ListCreateAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class TransactionDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

# Categories
class CategoryListCreateView(generics.ListCreateAPIView):
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)