from django.contrib import admin
from .models import CustomUser

# ลงทะเบียนโมเดลใน Django Admin
admin.site.register(CustomUser)  # หากต้องการให้ CustomUser ปรากฏใน Admin


from django.contrib import admin
from .models import Pig, BreedingRecord

@admin.register(Pig)
class PigAdmin(admin.ModelAdmin):
    list_display = ('pig_id', 'name', 'status', 'zone')

@admin.register(BreedingRecord)
class BreedingRecordAdmin(admin.ModelAdmin):
    list_display = ('pig', 'breeding_date', 'semen_id', 'delivery_date')
