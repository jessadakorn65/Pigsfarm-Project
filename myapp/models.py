from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # กำหนดตัวเลือกบทบาท (Role Choices)
    ROLE_CHOICES = (
        ('boss', 'หัวหน้า'),
        ('employee', 'พนักงาน'),
    )
    
    # ฟิลด์ role สำหรับตรวจสอบว่าผู้ใช้เป็นหัวหน้าหรือพนักงาน
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, null=True, blank=True)
    
    # ฟิลด์เลขบัตรประชาชน
    id_card = models.CharField(max_length=13, unique=True, null=True, blank=True)
    
    # ฟิลด์เบอร์โทร
    phone_number = models.CharField(max_length=10, null=True, blank=True)
    
    # ฟังก์ชันแสดงบทบาทและข้อมูลผู้ใช้
    def __str__(self):
        return f'{self.username} ({self.get_role_display()}) - ID: {self.id_card} - Phone: {self.phone_number}'

#----------------------------------------------------------------------
from django.db import models

# ตาราง pigs
from django.db import models
from datetime import timedelta

from django.db import models
from datetime import timedelta

class Pig(models.Model):
    pig_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    status = models.CharField(
        max_length=50,
        choices=[('ready', 'Ready for Breeding'), ('waiting', 'Waiting for Delivery')],
        default='ready'
    )
    zone = models.CharField(max_length=50)
    address_lock = models.CharField(max_length=100)
    image = models.ImageField(upload_to='pigs/', blank=True, null=True)  # เพิ่มฟิลด์สำหรับอัพโหลดรูปภาพ

    def __str__(self):
        return f"{self.pig_id} - {self.name}"


class BreedingRecord(models.Model):
    pig = models.ForeignKey(Pig, on_delete=models.CASCADE, related_name='breeding_records')
    breeding_date = models.DateField()
    semen_id = models.CharField(max_length=50)
    insemination_count = models.IntegerField(default=1)
    delivery_date = models.DateField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.delivery_date:
            self.delivery_date = self.breeding_date + timedelta(days=110)
        super().save(*args, **kwargs)

