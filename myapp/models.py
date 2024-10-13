from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('boss', 'หัวหน้า'),
        ('employee', 'พนักงาน'),
    )
    # ฟิลด์ role ที่จะใช้ในการตรวจสอบว่าเป็นหัวหน้าหรือพนักงาน
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, null=True, blank=True)
