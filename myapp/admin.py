from django.contrib import admin
from .models import CustomUser, Pig, BreedingRecord

# ลงทะเบียน CustomUser ใน Django Admin
admin.site.register(CustomUser)  # หากต้องการให้ CustomUser ปรากฏใน Admin

# ลงทะเบียนโมเดล Pig
@admin.register(Pig)
class PigAdmin(admin.ModelAdmin):
    list_display = ('pig_id', 'name', 'status', 'weight')  # เปลี่ยนจาก 'zone' เป็น 'weight'

# ลงทะเบียนโมเดล BreedingRecord
@admin.register(BreedingRecord)
class BreedingRecordAdmin(admin.ModelAdmin):
    list_display = ('pig', 'breeding_date', 'semen_id', 'delivery_date')