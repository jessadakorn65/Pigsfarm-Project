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

    # ฟิลด์โปรไฟล์รูปภาพ
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)  # กำหนด path สำหรับเก็บภาพ

    # ฟังก์ชันแสดงบทบาทและข้อมูลผู้ใช้
    def __str__(self):
        return f'{self.username} ({self.get_role_display()}) - ID: {self.id_card} - Phone: {self.phone_number}'


#-----------------------------------------------------------------------------------------------------------------
# ตาราง pigs

from django.db import models
from datetime import timedelta

from django.db import models
from datetime import timedelta

class Pig(models.Model):
    PIG_STATUS_CHOICES = [
        ('not_bred', 'ยังไม่ผสม'),
        ('ready', 'พร้อมผสม'),
        ('bred', 'ผสมแล้ว'),
        ('delivered', 'คลอดแล้ว'),
    ]
    
    pig_id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=100)
    status = models.CharField(
        max_length=50,
        choices=PIG_STATUS_CHOICES,
        default='not_bred'  
    )

    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # น้ำหนักหมู
    address_lock = models.CharField(max_length=100)
    image = models.ImageField(upload_to='pigs/', blank=True, null=True)

    # ฟิลด์ใหม่
    is_genital_swollen = models.BooleanField(default=False)  # อวัยวะเพศบวมไหม
    is_in_heat = models.BooleanField(default=False)  # ขี่หลังแล้วมีอาการฮีสติดสัดไหม

    def __str__(self):
        return f"{self.pig_id} - {self.name}"

    def update_status(self):
        if self.is_genital_swollen and self.is_in_heat:
            self.status = "bred"
        else:
            self.status = "not_bred"
        self.save()




class BreedingRecord(models.Model):
    pig = models.ForeignKey(Pig, on_delete=models.CASCADE, related_name='breeding_records', to_field="pig_id")
    breeding_date = models.DateField()
    semen_id = models.CharField(max_length=50)
    # ข้อมูลการคลอด
    delivery_date = models.DateField(blank=True, null=True)
    birth_time = models.TimeField(blank=True, null=True)  # เวลาที่คลอด
    alive_piglets = models.IntegerField(default=0)  
    dead_piglets = models.IntegerField(default=0)  
    deformed_piglets = models.IntegerField(default=0)
    notes = models.TextField(blank=True, null=True)  # โน้ตเพิ่มเติม
    export_date = models.DateTimeField(null=True, blank=True)  # ✅ เพิ่มฟิลด์นี้
    # ✅ ฟิลด์ใหม่สำหรับวันที่คลอดจริง
    actual_date = models.DateField(blank=True, null=True)
    


    @property
    def total_piglets(self):
        """ คำนวณจำนวนลูกสุกรทั้งหมดจากผลรวมของหมูรอด, ตาย, พิการ """
        return self.alive_piglets + self.dead_piglets + self.deformed_piglets

    def save(self, *args, **kwargs):
        # คำนวณวันที่คลอดถ้าไม่ได้ระบุ
        if not self.delivery_date:
            self.delivery_date = self.breeding_date + timedelta(days=110)
        
        super().save(*args, **kwargs)



class PigQueue(models.Model):
    pig = models.ForeignKey(Pig, on_delete=models.CASCADE, related_name='queues', to_field="pig_id")  
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.pig.pig_id} - {self.pig.name}"
    

