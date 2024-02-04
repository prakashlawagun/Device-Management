from django.urls import path
from .views import RegisterView, LoginView, EmployeeView, EmployeeDetailView, DeviceView, DeviceDetailView,DeviceLogDetailView,DeviceLogListCreateView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('employees/', EmployeeView.as_view(), name='employee-list'),
    path('employees/<int:pk>/', EmployeeDetailView.as_view(), name='employee-detail'),
    path('devices/', DeviceView.as_view(), name='device-list'),
    path('devices/<int:pk>/', DeviceDetailView.as_view(), name='device-detail'),
    path('devicelogs/', DeviceLogListCreateView.as_view(), name='devicelog-list-create'),
    path('devicelogs/<int:pk>/', DeviceLogDetailView.as_view(), name='devicelog-detail'),
]
