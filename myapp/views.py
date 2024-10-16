from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm

# ฟังก์ชันเข้าสู่ระบบ
def custom_login(request):
    if request.method == "POST":
        # รับค่าชื่อผู้ใช้และรหัสผ่านจากฟอร์ม
        username = request.POST['username']
        password = request.POST['password']
        # ตรวจสอบผู้ใช้
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # ล็อกอินหากผู้ใช้ถูกต้อง
            login(request, user)
            # ตรวจสอบบทบาทของผู้ใช้
            if user.role == 'boss':
                return redirect('boss_dashboard')  # ย้ายไปที่หน้าแดชบอร์ดของเจ้านาย
            elif user.role == 'employee':
                return redirect('employee_dashboard')  # ย้ายไปที่หน้าแดชบอร์ดของพนักงาน
        else:
            # หากข้อมูลไม่ถูกต้อง ให้แสดงข้อผิดพลาด
            return render(request, 'myapp/login.html', {'error': 'Invalid credentials'})  # เส้นทางหน้าเข้าสู่ระบบ

    # แสดงหน้าเข้าสู่ระบบเริ่มต้น
    return render(request, 'myapp/login.html')  # เส้นทางหน้าเข้าสู่ระบบ

# ฟังก์ชันสำหรับหน้าแดชบอร์ดของพนักงาน (ต้องล็อกอิน)
@login_required
def employee_dashboard(request):
    return render(request, 'myapp/employee_dashboard.html')

# ฟังก์ชันสำหรับหน้าแดชบอร์ดของเจ้านาย (ต้องล็อกอิน)
@login_required
def boss_dashboard(request):
    return render(request, 'myapp/boss_dashboard.html')

# ฟังก์ชันสำหรับหน้าแรกของเว็บ
def home(request):
    return render(request, 'myapp/home.html')  # ยืนยันว่าเส้นทางไฟล์ถูกต้อง

# ฟังก์ชันสมัครสมาชิกใหม่
def register(request):
    if request.method == 'POST':
        # หากเป็นคำขอ POST ให้สร้างฟอร์มด้วยข้อมูลที่ได้รับ
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # หากฟอร์มถูกต้อง ให้บันทึกผู้ใช้ใหม่
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # ตั้งรหัสผ่านเข้ารหัส
            user.save()
            return redirect('login')  # เปลี่ยนไปที่หน้าล็อกอินหลังจากสมัครสำเร็จ
    else:
        # หากเป็นคำขอ GET ให้สร้างฟอร์มเปล่า
        form = CustomUserCreationForm()

    # แสดงหน้าสมัครสมาชิก พร้อมส่งฟอร์มไปแสดงในเทมเพลต
    return render(request, 'myapp/register.html', {'form': form})

# ฟังก์ชันแสดงหน้าเข้าสู่ระบบ (สำหรับหน้าเข้าสู่ระบบปกติ)
def login_view(request):
    return render(request, 'myapp/login.html')  # เส้นทางหน้าเข้าสู่ระบบ
