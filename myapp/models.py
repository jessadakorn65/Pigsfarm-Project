from django.contrib.auth.models import AbstractUser
from django.db import models

# สร้างโมเดล CustomUser โดยสืบทอดจาก AbstractUser
class CustomUser(AbstractUser):
    # กำหนดตัวเลือกบทบาท (Role Choices)
    ROLE_CHOICES = (
        ('boss', 'หัวหน้า'),
        ('employee', 'พนักงาน'),
    )
    
    # ฟิลด์ role สำหรับตรวจสอบว่าผู้ใช้เป็นหัวหน้าหรือพนักงาน
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, null=True, blank=True)

    # ฟังก์ชันแสดงบทบาทของผู้ใช้ (อาจใช้ในการตรวจสอบบทบาทเพิ่มเติม)
    def __str__(self):
        return f'{self.username} ({self.get_role_display()})'
