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
from .models import Pig, BreedingRecord
from .forms import BreedingRecordForm



def record_breeding(request, pig_id):
    pig = get_object_or_404(Pig, pig_id=pig_id)
    if request.method == 'POST':
        form = BreedingRecordForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.pig = pig
            record.save()
            return render(request, 'myapp/delivery_popup.html', {'delivery_date': record.delivery_date})
    else:
        form = BreedingRecordForm()
    return render(request, 'myapp/record_breeding.html', {'pig': pig, 'form': form})

from django.shortcuts import render, get_object_or_404
from .models import Pig

# ฟังก์ชันแสดงประวัติการผสม
def breeding_history(request, pig_id):
    pig = get_object_or_404(Pig, pig_id=pig_id)  # ดึงข้อมูลหมูตาม pig_id
    breeding_records = pig.breeding_records.all()  # ดึงข้อมูลประวัติการผสมทั้งหมดที่เชื่อมโยงกับหมูตัวนี้

    # ส่งข้อมูลไปที่เทมเพลต
    return render(request, 'myapp/breeding_history.html', {
        'pig': pig,
        'breeding_records': breeding_records
    })

from django.shortcuts import get_object_or_404, redirect
from .models import BreedingRecord

# ฟังก์ชันสำหรับลบประวัติการผสม
def delete_breeding_record(request, record_id):
    record = get_object_or_404(BreedingRecord, id=record_id)
    record.delete()  # ลบประวัติการผสม
    return redirect('breeding_history', pig_id=record.pig.pig_id)  # กลับไปที่หน้าประวัติการผสมของหมู

from django.shortcuts import render
from .models import Pig

from django.db.models import Q  # สำหรับการค้นหาที่ซับซ้อน

def pig_list(request):
    # รับค่าพารามิเตอร์จาก URL
    query = request.GET.get('q', '')  # คำค้นหา
    status_filter = request.GET.get('status', '')  # สถานะ (ready หรือ waiting)
    zone_filter = request.GET.get('zone', '')  # โซน

    pigs = Pig.objects.all()

    # ใช้ฟิลเตอร์ทีละขั้นตอน
    if query:
        pigs = pigs.filter(Q(pig_id__icontains=query) | Q(name__icontains=query))
    if status_filter:
        pigs = pigs.filter(status=status_filter)
    if zone_filter:
        pigs = pigs.filter(zone__icontains=zone_filter)

    # ส่งข้อมูลไปยังเทมเพลต
    return render(request, 'myapp/pig_list.html', {'pigs': pigs})


from django.shortcuts import render, get_object_or_404, redirect
from .models import Pig
from .forms import PigForm  # สมมติว่าคุณมีแบบฟอร์มสำหรับแก้ไขข้อมูลหมู

def edit_pig(request, pig_id):
    pig = get_object_or_404(Pig, pig_id=pig_id)  # ดึงข้อมูลหมูตาม ID
    if request.method == 'POST':
        form = PigForm(request.POST, request.FILES, instance=pig)  # อัปเดตข้อมูลหมู
        if form.is_valid():
            form.save()
            return redirect('pig_list')  # เปลี่ยนไปหน้ารายการหมูหลังจากแก้ไข
    else:
        form = PigForm(instance=pig)  # สร้างฟอร์มพร้อมข้อมูลเดิม
    return render(request, 'myapp/edit_pig.html', {'form': form, 'pig': pig})

from django.shortcuts import get_object_or_404, redirect
from .models import Pig

def delete_pig(request, pig_id):
    pig = get_object_or_404(Pig, pig_id=pig_id)  # ดึงข้อมูลหมูตาม ID
    if request.method == "POST":
        pig.delete()  # ลบข้อมูลหมู
        return redirect('pig_list')  # กลับไปยังหน้ารายการหมู
    return render(request, 'myapp/delete_pig.html', {'pig': pig})

from django.shortcuts import render, redirect
from .models import Pig
from .forms import PigForm  # ฟอร์มที่ใช้สำหรับเพิ่มหมู

def add_pig(request):
    if request.method == 'POST':
        form = PigForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # บันทึกข้อมูลหมู
            return redirect('pig_list')  # กลับไปหน้ารายการหมู
    else:
        form = PigForm()
    return render(request, 'myapp/add_pig.html', {'form': form})