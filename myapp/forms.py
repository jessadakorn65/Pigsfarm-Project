from django import forms
from .models import CustomUser
from .models import Pig  # นำเข้าโมเดล Pig จาก models.py
from django.contrib.auth.hashers import make_password  # นำเข้าเพื่อเข้ารหัสคำตอบลับ



class CustomUserCreationForm(forms.ModelForm):
    # ฟิลด์สำหรับรหัสผ่านและยืนยันรหัสผ่าน
    password = forms.CharField(widget=forms.PasswordInput, label='Password')
    password_confirm = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')

    # ฟิลด์เลขบัตรประชาชนและเบอร์โทร
    id_card = forms.CharField(max_length=13, required=False, widget=forms.TextInput(attrs={'placeholder': 'เลขบัตรประชาชน'}))
    phone_number = forms.CharField(max_length=10, required=False, widget=forms.TextInput(attrs={'placeholder': 'เบอร์โทร'}))

    # ✅ เพิ่มฟิลด์คำถามลับและคำตอบลับ
    secret_question = forms.CharField(max_length=255, required=True, label="คำถามลับ", help_text="เช่น 'สัตว์เลี้ยงตัวแรกของคุณชื่ออะไร?'")
    secret_answer = forms.CharField(widget=forms.PasswordInput, required=True, label="คำตอบลับ")

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password', 'password_confirm', 'role', 'id_card', 'phone_number', 'secret_question', 'secret_answer')

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords do not match.")
        
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])  # ✅ เข้ารหัสรหัสผ่าน
        user.secret_answer = make_password(self.cleaned_data["secret_answer"])  # ✅ เข้ารหัสคำตอบลับ
        if commit:
            user.save()
        return user



    

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
        fields = ['actual_date', 'birth_time', 'alive_piglets', 'dead_piglets', 'deformed_piglets']
        labels = {
            'actual_date': '📅 วันที่คลอดจริง',
            'birth_time': '⏰ เวลาคลอด',
            'alive_piglets': '🐖 จำนวนหมูรอด',
            'dead_piglets': '☠️ จำนวนหมูตาย',
            'deformed_piglets': '⚠️ จำนวนหมูพิการ',
        }
        widgets = {
            'actual_date': forms.DateInput(attrs={'type': 'date', 'class': 'border rounded p-2 w-full'}),
            'birth_time': forms.TimeInput(attrs={'type': 'time', 'class': 'border rounded p-2 w-full'}),
            'alive_piglets': forms.NumberInput(attrs={'class': 'border rounded p-2 w-full'}),
            'dead_piglets': forms.NumberInput(attrs={'class': 'border rounded p-2 w-full'}),
            'deformed_piglets': forms.NumberInput(attrs={'class': 'border rounded p-2 w-full'}),
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
        fields = ['username', 'email', 'role', 'id_card', 'phone_number']


class PasswordResetForm(forms.Form):
    username = forms.CharField(max_length=150, label="Username")
    secret_answer = forms.CharField(widget=forms.PasswordInput, label="Secret Answer")
    new_password = forms.CharField(widget=forms.PasswordInput, label="New Password")
    confirm_new_password = forms.CharField(widget=forms.PasswordInput, label="Confirm New Password")

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_new_password = cleaned_data.get("confirm_new_password")

        if new_password and confirm_new_password and new_password != confirm_new_password:
            raise forms.ValidationError("New passwords do not match.")

        return cleaned_data
