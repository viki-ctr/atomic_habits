from django.urls import path

from users.views import UserDetailView, UserRegisterView

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='user-register'),
    path('me/', UserDetailView.as_view(), name='user-detail'),
]
