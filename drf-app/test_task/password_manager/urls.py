from django.urls import path
from test_task.password_manager.views import PasswordEntryView, PasswordEntryRetrieveView, password_api_root

urlpatterns = [
    path('', password_api_root, name='password-api-root'),
    path('password/', PasswordEntryView.as_view(), name='password-list-create'),
    path('password/<str:service_name>/', PasswordEntryRetrieveView.as_view(), name='password-retrieve'),
]