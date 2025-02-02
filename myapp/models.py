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

#-----------------------------------------------------------------------------------------------------------------
# ตาราง pigs

from django.db import models
from datetime import timedelta
# models.py
from django.db import models

class Pig(models.Model):
    PIG_STATUS_CHOICES = [
        ('not_bred', 'ยังไม่ผสม'),
        ('ready', 'พร้อมผสม'),
        ('bred', 'ผสมแล้ว'),
        ('waiting', 'รอคลอด'),
    ]
    pig_id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=100)
    status = models.CharField(
        max_length=50,
        choices=PIG_STATUS_CHOICES,
        default='not_bred'  # ค่าเริ่มต้นเป็นยังไม่ผสม
    )
    zone = models.CharField(max_length=50)
    address_lock = models.CharField(max_length=100)
    image = models.ImageField(upload_to='pigs/', blank=True, null=True)

    def __str__(self):
        return f"{self.pig_id} - {self.name}"

    # ฟังก์ชันเพื่อเปลี่ยนสถานะหมูอัตโนมัติ
    def update_status(self):
        if self.status == 'ready' and self.pig_id not in PigQueue.objects.filter(pig=self).values_list('pig', flat=True):
            self.status = 'not_bred'  # ยังไม่ผสม
        self.save()



class BreedingRecord(models.Model):
    pig = models.ForeignKey(Pig, on_delete=models.CASCADE, related_name='breeding_records', to_field="pig_id")
    breeding_date = models.DateField()
    semen_id = models.CharField(max_length=50)
    insemination_count = models.IntegerField(default=1)
    delivery_date = models.DateField(blank=True, null=True)
    total_piglets = models.IntegerField(default=0)  # บันทึกจำนวนลูกสุกรทั้งหมด

    def save(self, *args, **kwargs):
        if not self.delivery_date:
            self.delivery_date = self.breeding_date + timedelta(days=110)
        super().save(*args, **kwargs)

class Piglet(models.Model):
    breeding_record = models.ForeignKey(BreedingRecord, on_delete=models.CASCADE, related_name='piglets')
    pig = models.ForeignKey(Pig, on_delete=models.CASCADE, related_name='pig_piglets', to_field="pig_id")
    semen_id = models.CharField(max_length=50, null=True, blank=True)
    birth_date = models.DateField()
    alive_count = models.IntegerField(default=0)
    dead_count = models.IntegerField(default=0)
    deformed_count = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        # อัปเดตจำนวนลูกสุกรทั้งหมดใน BreedingRecord
        self.breeding_record.total_piglets = self.alive_count + self.dead_count + self.deformed_count
        self.breeding_record.save()
        super().save(*args, **kwargs)


class PigQueue(models.Model):
    pig = models.ForeignKey(Pig, on_delete=models.CASCADE, related_name='queues', to_field="pig_id")  
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.pig.pig_id} - {self.pig.name}"
