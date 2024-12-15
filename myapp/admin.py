from django.contrib import admin
from .models import CustomUser, Pig  # นำเข้าโมเดล CustomUser และ Pig

# ลงทะเบียนโมเดลใน Django Admin
admin.site.register(CustomUser)  # หากต้องการให้ CustomUser ปรากฏใน Admin
admin.site.register(Pig)  # ลงทะเบียนโมเดล Pig
