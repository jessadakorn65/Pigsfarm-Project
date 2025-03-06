from django import forms
from .models import CustomUser
from .models import Pig  # นำเข้าโมเดล Pig จาก models.py

# ฟอร์มสร้างผู้ใช้ใหม่ที่ใช้ CustomUser model
class CustomUserCreationForm(forms.ModelForm):
    # ฟิลด์สำหรับรหัสผ่านและยืนยันรหัสผ่าน
    password = forms.CharField(widget=forms.PasswordInput, label='Password')
    password_confirm = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')

    # ฟิลด์เลขบัตรประชาชนและเบอร์โทร
    id_card = forms.CharField(max_length=13, required=False, widget=forms.TextInput(attrs={'placeholder': 'เลขบัตรประชาชน'}))
    phone_number = forms.CharField(max_length=10, required=False, widget=forms.TextInput(attrs={'placeholder': 'เบอร์โทร'}))

    # ฟิลด์รูปโปรไฟล์
    profile_picture = forms.ImageField(required=False)  # เพิ่มฟิลด์สำหรับการอัปโหลดรูปภาพโปรไฟล์

    # Meta class สำหรับกำหนดฟิลด์ที่ต้องการจากโมเดล CustomUser
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password', 'password_confirm', 'role', 'id_card', 'phone_number', 'profile_picture')

    # ฟังก์ชัน clean สำหรับตรวจสอบข้อมูลที่กรอกเข้ามา
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        # ตรวจสอบว่ารหัสผ่านและรหัสผ่านยืนยันตรงกันหรือไม่
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords do not match.")
        
        return cleaned_data

    

from django import forms
from .models import Pig  # นำเข้าโมเดล Pig จากไฟล์ models.py

class PigForm(forms.ModelForm):
    class Meta:
        model = Pig  # ใช้โมเดล Pig
        fields = ['pig_id', 'name', 'status', 'weight', 'address_lock', 'image']  # ใช้ฟิลด์ที่ต้องการ
        widgets = {
            'pig_id': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control'}),  # ใช้ NumberInput สำหรับน้ำหนัก
            'address_lock': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }



from django import forms
from .models import BreedingRecord

class BreedingRecordForm(forms.ModelForm):
    class Meta:
        model = BreedingRecord
        fields = ['breeding_date', 'semen_id', 'notes',]  # เอา insemination_count ออก
        widgets = {
            'breeding_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'semen_id': forms.TextInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }



from django import forms
from .models import BreedingRecord

class PigletRecordForm(forms.ModelForm):
    class Meta:
        model = BreedingRecord
        fields = ['delivery_date', 'birth_time', 'alive_piglets', 'dead_piglets', 'deformed_piglets']
        labels = {
            'delivery_date': 'วันที่คลอด',
            'birth_time': 'เวลาคลอด',
            'alive_piglets': 'จำนวนหมูรอด',
            'dead_piglets': 'จำนวนหมูตาย',
            'deformed_piglets': 'จำนวนหมูพิการ',
        }
        widgets = {
            'delivery_date': forms.DateInput(attrs={'type': 'date', 'class': 'border rounded p-1'}),
            'birth_time': forms.TimeInput(attrs={'type': 'time', 'class': 'border rounded p-1'}),
            'alive_piglets': forms.NumberInput(attrs={'class': 'border rounded p-1 w-16'}),
            'dead_piglets': forms.NumberInput(attrs={'class': 'border rounded p-1 w-16'}),
            'deformed_piglets': forms.NumberInput(attrs={'class': 'border rounded p-1 w-16'}),
        }

# myapp/forms.py
from django import forms

class CheckHeatStatusForm(forms.Form):
    GENITAL_CHOICES = [
        ('yes', 'ใช่'),
        ('no', 'ไม่ใช่')
    ]
    is_genital_swollen = forms.ChoiceField(choices=GENITAL_CHOICES, widget=forms.RadioSelect, label='อวัยวะเพศบวมไหม?')
    is_in_heat = forms.ChoiceField(choices=GENITAL_CHOICES, widget=forms.RadioSelect, label='ขี่หลังแล้วมีอาการฮีสติดสัดไหม?')


from django import forms
from .models import CustomUser

class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'profile_picture', 'role', 'id_card', 'phone_number']

