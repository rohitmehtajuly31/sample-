from django.db import models
from django.contrib.auth.models import User
import random

class OTP(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp_code = models.CharField(max_length=6, default='')

    def generate_otp(self):
        self.otp_code = str(random.randint(100000, 999999))
        self.save()
