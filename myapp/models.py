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
    
    # ข้อมูลการคลอด
    delivery_date = models.DateField(blank=True, null=True)
    birth_time = models.TimeField(blank=True, null=True)  # เวลาที่คลอด
    alive_piglets = models.IntegerField(default=0)  
    dead_piglets = models.IntegerField(default=0)  
    deformed_piglets = models.IntegerField(default=0)

    # เพิ่มฟิลด์รูปภาพและโน้ต
    insemination_image = models.ImageField(upload_to='insemination_images/', blank=True, null=True)  # เก็บรูป
    notes = models.TextField(blank=True, null=True)  # โน้ตเพิ่มเติม

    @property
    def total_piglets(self):
        """ คำนวณจำนวนลูกสุกรทั้งหมดจากผลรวมของหมูรอด, ตาย, พิการ """
        return self.alive_piglets + self.dead_piglets + self.deformed_piglets

    def save(self, *args, **kwargs):
        # คำนวณวันที่คลอดถ้าไม่ได้ระบุ
        if not self.delivery_date:
            self.delivery_date = self.breeding_date + timedelta(days=110)
        
        # ตรวจสอบการผสมครั้งก่อนและอัปเดตจำนวนครั้งการผสม
        if not self.insemination_count:
            previous_record = BreedingRecord.objects.filter(pig=self.pig).order_by('-breeding_date').first()
            if previous_record:
                self.insemination_count = previous_record.insemination_count + 1
            else:
                self.insemination_count = 1

        super().save(*args, **kwargs)






class PigQueue(models.Model):
    pig = models.ForeignKey(Pig, on_delete=models.CASCADE, related_name='queues', to_field="pig_id")  
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.pig.pig_id} - {self.pig.name}"
