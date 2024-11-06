from django.urls import path

from main import views

app_name = 'main'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('confirm-email/<uidb64>/<token>/', views.confirm_email, name='confirm_email'),
]
