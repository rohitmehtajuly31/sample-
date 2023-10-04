from django.urls import path
from . import views

urlpatterns = [

    path('send_otp/', views.send_otp, name='send_otp'),
    path('verify_otp/', views.verify_otp, name='verify_otp'),
    path('login_with_otp/<str:email>/', views.login_with_otp, name='login_with_otp')
    # Add more app-specific URL patterns here
]
