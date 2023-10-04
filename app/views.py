# from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required
# from django.core.mail import send_mail
# from django.contrib.auth.models import User
# from .models import OTP


# def send_otp(request):
#     user = request.user
#     print("--",user)
    
#     otp, created = OTP.objects.get_or_create(user=user)
#     print("otp",otp)
#     otp.generate_otp()
#     print(otp.otp_code)

  
#     send_mail(
#         'OTP Verification',
#         f'Your OTP is: {otp.otp_code}',
#         'rohit@snakescript.com',
#         [user.email],
#         fail_silently=False,
#     )
#     return render(request, 'otp_form.html')


# def verify_otp(request):
#     user = request.user
#     otp = OTP.objects.get(user=user)
#     if request.method == 'POST':
#         otp_code = request.POST['otp']
#         if otp.otp_code == otp_code:
#             otp.delete()
#             return redirect('success_page')
#     return render(request, 'error.html', {'error': 'Invalid OTP'})


# def success_page(request):
#     return render(request, 'success_page.html')




from django.shortcuts import render, redirect
from .models import OTP
from django.core.mail import send_mail
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# def send_otp(request):
#     if request.method == 'POST':
#         email = request.POST['email']
#         otp, created = OTP.objects.get_or_create(email=email)
#         otp.generate_otp()
#         send_mail(
#             'OTP Verification',
#             f'Your OTP is: {otp.otp_code}',
#             'your-email@example.com',
#             [email],
#             fail_silently=False,
#         )
#         return redirect('verify_otp')
#     return render(request, 'send_otp.html')

def send_otp(request):
    if request.method == 'POST':
        email = request.POST['email']
        try:
            user = User.objects.get(email=email)  # Fetch the user based on email
            otp, created = OTP.objects.get_or_create(user=user)  # Create or get the OTP object associated with the user
            otp.generate_otp()
            send_mail(
                'OTP Verification',
                f'Your OTP is: {otp.otp_code}',
                'rohitmehta31july@gmail.com',
                [email],
                fail_silently=False,
            )
            return redirect('verify_otp')
        except User.DoesNotExist:
            return render(request, 'error.html', {'error': 'User not found.'})
    return render(request, 'send_otp.html')

def verify_otp(request):
    if request.method == 'POST':
        email = request.POST['email']
        otp_code = request.POST['otp']
        try:
            user = User.objects.get(email=email)  # Fetch the User object based on email
            otp = OTP.objects.get(user=user)  # Use the User object to fetch the related OTP
            if otp.otp_code == otp_code:
                otp.delete()
                return redirect('login_with_otp', email=email)
        except User.DoesNotExist:
            return render(request, 'error.html', {'error': 'User not found.'})
        except OTP.DoesNotExist:
            return render(request, 'error.html', {'error': 'Invalid OTP.'})
    return render(request, 'verify_otp.html')


def login_with_otp(request, email):
    try:
        user = User.objects.get(email=email)
        login(request, user)
        return render(request, 'success_page.html')
    except User.DoesNotExist:
        return render(request, 'error.html', {'error': 'User not found.'})
