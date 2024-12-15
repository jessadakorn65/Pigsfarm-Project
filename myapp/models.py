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
class Pig(models.Model):
    id = models.AutoField(primary_key=True)
    img = models.ImageField(upload_to='pig_images/', blank=True, null=True)
    pig_id = models.CharField(max_length=50)
    address_lock = models.CharField(max_length=255)
    zone = models.CharField(max_length=5)
    status = models.CharField(
        max_length=10,
        choices=[('ปกติ', 'ปกติ'), ('ผสมแล้ว', 'ผสมแล้ว')],
        default='ปกติ'
    )

    def __str__(self):
        return self.pig_id

# ตาราง inseminations
class Insemination(models.Model):
    inseminations_id = models.AutoField(primary_key=True)
    pig = models.ForeignKey(Pig, on_delete=models.CASCADE)
    insemination_date = models.DateField()
    semen_id = models.CharField(max_length=50)
    img = models.ImageField(upload_to='insemination_images/', blank=True, null=True)
    insemination_result = models.CharField(
        max_length=10,
        choices=[('สำเร็จ', 'สำเร็จ'), ('ล้มเหลว', 'ล้มเหลว')],
        default='ล้มเหลว'
    )
    notes = models.TextField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Insemination {self.inseminations_id} for Pig {self.pig.pig_id}"

