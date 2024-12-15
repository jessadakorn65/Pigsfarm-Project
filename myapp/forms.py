from django import forms
from .models import CustomUser

from django import forms
from .models import CustomUser

# ฟอร์มสร้างผู้ใช้ใหม่ที่ใช้ CustomUser model
class CustomUserCreationForm(forms.ModelForm):
    # ฟิลด์สำหรับรหัสผ่านและยืนยันรหัสผ่าน
    password = forms.CharField(widget=forms.PasswordInput, label='Password')
    password_confirm = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')

    # ฟิลด์เลขบัตรประชาชนและเบอร์โทร
    id_card = forms.CharField(max_length=13, required=False, widget=forms.TextInput(attrs={'placeholder': 'เลขบัตรประชาชน'}))
    phone_number = forms.CharField(max_length=10, required=False, widget=forms.TextInput(attrs={'placeholder': 'เบอร์โทร'}))

    # Meta class สำหรับกำหนดฟิลด์ที่ต้องการจากโมเดล CustomUser
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password', 'password_confirm', 'role', 'id_card', 'phone_number')

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
from .models import Insemination

class InseminationForm(forms.ModelForm):
    class Meta:
        model = Insemination
        fields = ['insemination_date', 'semen_id', 'img', 'insemination_result', 'notes']
        widgets = {
            'insemination_date': forms.DateInput(attrs={'type': 'date'}),
        }
