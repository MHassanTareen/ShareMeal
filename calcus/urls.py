from django.urls import path
from .views import BillListView, BillCreateView, UserBalanceView,BillDetailView,UserCreateView, UserDetailView

urlpatterns = [
    path('', BillListView.as_view(), name='bills-list'),
    path('create/', BillCreateView.as_view(), name='bill-create'),
    path('balances/', UserBalanceView.as_view(), name='user-balances'),
    path('<uuid:uuid>/', BillDetailView.as_view(), name='bill-detail'),
    path('user/add/', UserCreateView.as_view(), name='user-create'),
    path('user/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    
]