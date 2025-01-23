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
#-------------------------------------------------------------------------------------------------------------------------------------------------
from django.shortcuts import render, get_object_or_404, redirect
from .models import Pig, Insemination
from .forms import InseminationForm

# ฟังก์ชันค้นหาสุกร
def search_pigs(request):
    query = request.GET.get('q')  # รับคีย์เวิร์ดที่กรอกในช่องค้นหา
    pigs = None
    if query:
        pigs = Pig.objects.filter(pig_id__icontains=query)
    return render(request, 'myapp/search_pigs.html', {'pigs': pigs})

# ฟังก์ชันบันทึกข้อมูลการผสม
def insemination_record(request, pig_id):
    pig = get_object_or_404(Pig, id=pig_id)
    if request.method == 'POST':
        form = InseminationForm(request.POST, request.FILES)
        if form.is_valid():
            insemination = form.save(commit=False)
            insemination.pig = pig
            insemination.save()
            return redirect('pig_detail', pig_id=pig.id)
    else:
        form = InseminationForm()
    return render(request, 'myapp/insemination_record.html', {'form': form, 'pig': pig})

from django.shortcuts import render, get_object_or_404
from .models import Pig, Insemination

def pig_detail(request, pig_id):
    pig = get_object_or_404(Pig, id=pig_id)
    inseminations = Insemination.objects.filter(pig=pig)
    return render(request, 'myapp/pig_detail.html', {'pig': pig, 'inseminations': inseminations})


from django.shortcuts import render, redirect
from .forms import PigForm

# เพิ่มหมูใหม่
def add_pig(request):
    if request.method == 'POST':
        form = PigForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('search_pigs')  # กลับไปที่หน้าค้นหาหมู
    else:
        form = PigForm()
    return render(request, 'myapp/add_pig.html', {'form': form})


def pig_list(request):
    pigs = Pig.objects.all()  # ดึงข้อมูลสุกรทั้งหมดจากฐานข้อมูล
    return render(request, 'myapp/pig_list.html', {'pigs': pigs})

from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Pig, Insemination

@login_required
def add_insemination(request, pig_id):
    pig = Pig.objects.get(pig_id=pig_id)
    if request.method == 'POST':
        insemination_date = request.POST.get('insemination_date')
        semen_id = request.POST.get('semen_id')
        notes = request.POST.get('notes', '')

        # สร้างบันทึกการผสม
        insemination = Insemination(
            pig=pig,
            insemination_date=insemination_date,
            semen_id=semen_id,
            notes=notes,
            recorded_by=request.user  # บันทึกผู้ใช้ที่ล็อกอิน
        )
        insemination.save()

        # อัปเดตสถานะหมู
        pig.status = 'pregnant'
        pig.save()

        # ส่งข้อความป๊อปอัพ
        messages.success(request, f"บันทึกสำเร็จ! วันที่คาดว่าจะคลอด: {insemination.expected_delivery_date}")

        return redirect('pig_list')

    return render(request, 'add_insemination.html', {'pig': pig})
