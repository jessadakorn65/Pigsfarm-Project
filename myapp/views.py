from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm

def custom_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if user.role == 'boss':
                return redirect('boss_dashboard')
            elif user.role == 'employee':
                return redirect('employee_dashboard')
        else:
            return render(request, 'myapp/login.html', {'error': 'Invalid credentials'})  # แก้ไขเส้นทาง

    return render(request, 'myapp/login.html')  # แก้ไขเส้นทาง

from django.contrib.auth.decorators import login_required

@login_required
def employee_dashboard(request):
    return render(request, 'myapp/employee_dashboard.html')

@login_required
def boss_dashboard(request):
    return render(request, 'myapp/boss_dashboard.html')

def home(request):
    return render(request, 'myapp/home.html')  # ยืนยันว่าชื่อไฟล์ถูกต้อง

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # ตั้งรหัสผ่านที่เข้ารหัส
            user.save()
            return redirect('login')  # เปลี่ยนไปที่หน้าล็อกอินหลังจากสมัครสำเร็จ
    else:
        form = CustomUserCreationForm()

    return render(request, 'myapp/register.html', {'form': form})


def login_view(request):
    return render(request, 'myapp/login.html')  # ฟังก์ชันสำหรับแสดงหน้าเข้าสู่ระบบ
