from django import forms
from .models import CustomUser

# ฟอร์มสร้างผู้ใช้ใหม่ที่ใช้ CustomUser model
class CustomUserCreationForm(forms.ModelForm):
    # ฟิลด์สำหรับรหัสผ่านและยืนยันรหัสผ่าน
    password = forms.CharField(widget=forms.PasswordInput, label='Password')
    password_confirm = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')

    # Meta class สำหรับกำหนดฟิลด์ที่ต้องการจากโมเดล CustomUser
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password', 'role')

    # ฟังก์ชัน clean สำหรับตรวจสอบข้อมูลที่กรอกเข้ามา
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        # ตรวจสอบว่ารหัสผ่านและรหัสผ่านยืนยันตรงกันหรือไม่
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords do not match.")
