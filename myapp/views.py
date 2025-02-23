from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from .models import Pig, PigQueue

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
# views.py
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
            
            # เปลี่ยนสถานะหมูเป็น "ผสมแล้ว"
            pig.status = 'bred'
            pig.save()

            # ลบหมูตัวนี้ออกจากคิวหากมันอยู่ในคิว
            if pig.queues.exists():  # ตรวจสอบว่าหมูตัวนี้อยู่ในคิว
                pig.queues.all().delete()  # ลบหมูตัวนี้ออกจากคิวทั้งหมด

            return render(request, 'myapp/delivery_popup.html', {'delivery_date': record.delivery_date})
    else:
        form = BreedingRecordForm()
    return render(request, 'myapp/record_breeding.html', {'pig': pig, 'form': form})


def breeding_history(request, pig_id):
    pig = get_object_or_404(Pig, pig_id=pig_id)  # ใช้ pig_id เป็น primary key
    breeding_records = pig.breeding_records.all()  # ดึงข้อมูลประวัติการผสมทั้งหมดที่เชื่อมโยงกับหมูตัวนี้
    return render(request, 'myapp/breeding_history.html', {
        'pig': pig,
        'breeding_records': breeding_records
    })

def delete_breeding_record(request, record_id):
    record = get_object_or_404(BreedingRecord, id=record_id)
    record.delete()
    return redirect('breeding_history', pig_id=record.pig.pig_id)  # ใช้ pig_id

def pig_list(request):
    query = request.GET.get('q', '')
    status_filter = request.GET.get('status', '')
    zone_filter = request.GET.get('zone', '')
    pigs = Pig.objects.all()

    if query:
        pigs = pigs.filter(Q(pig_id__icontains=query) | Q(name__icontains=query))
    if status_filter:
        pigs = pigs.filter(status=status_filter)
    if zone_filter:
        pigs = pigs.filter(zone__icontains=zone_filter)

    return render(request, 'myapp/pig_list.html', {'pigs': pigs})

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from .models import Pig, BreedingRecord, PigQueue
from .forms import PigForm, BreedingRecordForm

def add_pig(request):
    if request.method == 'POST':
        form = PigForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('pig_list')
    else:
        form = PigForm()
    return render(request, 'myapp/add_pig.html', {'form': form})

def edit_pig(request, pig_id):
    pig = get_object_or_404(Pig, pig_id=pig_id)
    if request.method == 'POST':
        form = PigForm(request.POST, request.FILES, instance=pig)
        if form.is_valid():
            form.save()
            return redirect('pig_list')
    else:
        form = PigForm(instance=pig)
    return render(request, 'myapp/edit_pig.html', {'form': form, 'pig': pig})

def delete_pig(request, pig_id):
    pig = get_object_or_404(Pig, pig_id=pig_id)
    if request.method == "POST":
        pig.delete()
        return redirect('pig_list')
    return render(request, 'myapp/delete_pig.html', {'pig': pig})

def add_pig(request):
    if request.method == 'POST':
        form = PigForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('pig_list')
    else:
        form = PigForm()
    return render(request, 'myapp/add_pig.html', {'form': form})

# views.py
from django.shortcuts import get_object_or_404, redirect
from .models import Pig, PigQueue
from django.contrib import messages


from django.contrib import messages

from django.contrib import messages

def add_to_queue(request, pig_id):
    pig = get_object_or_404(Pig, pig_id=pig_id)
    if not pig.queues.exists():  # ถ้าไม่อยู่ในคิว
        pig.status = 'ready'
        pig.save()
        PigQueue.objects.create(pig=pig)
        messages.success(request, f"หมู {pig.pig_id} ({pig.name}) ได้รับการเพิ่มเข้าสู่คิวเรียบร้อยแล้ว!")
    else:
        messages.warning(request, f"หมู {pig.pig_id} ({pig.name}) อยู่ในคิวแล้ว!")

    return redirect('pig_queue')




def remove_from_queue(request, queue_id):
    queue_item = get_object_or_404(PigQueue, id=queue_id)
    queue_item.delete()
    messages.success(request, f"ลบสุกร {queue_item.pig.pig_id} ออกจากคิวสำเร็จ!")
    return redirect('pig_queue')

from django.shortcuts import render, get_object_or_404
from .models import Pig, PigQueue

def pig_queue(request):
    pigs = Pig.objects.all()  # หรือคิวที่เหมาะสม
    queue = PigQueue.objects.all().order_by('added_at')

    return render(request, 'myapp/pig_queue.html', {
        'queue': queue,
        'pig': pigs.first()  # ตัวอย่าง ถ้าคุณต้องการส่ง pig ไปที่หน้า
    })



from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Pig, BreedingRecord
from .forms import PigletRecordForm

def update_piglet_data(request, pig_id):
    pig = get_object_or_404(Pig, pig_id=pig_id)
    latest_breeding_record = pig.breeding_records.order_by('-breeding_date').first()  # เอาประวัติการผสมล่าสุด

    if not latest_breeding_record:
        messages.error(request, "ไม่พบประวัติการผสมสำหรับหมูตัวนี้")
        return redirect('breeding_history', pig_id=pig.pig_id)

    if request.method == "POST":
        form = PigletRecordForm(request.POST, instance=latest_breeding_record)
        if form.is_valid():
            form.save()
            # เมื่อบันทึกข้อมูลลูกสุกรแล้ว เปลี่ยนสถานะหมูเป็น 'คลอดแล้ว'
            pig.status = 'delivered'
            pig.save()
            messages.success(request, "บันทึกข้อมูลลูกสุกรสำเร็จ!")
            return redirect('breeding_history', pig_id=pig.pig_id)
    else:
        form = PigletRecordForm(instance=latest_breeding_record)

    return render(request, 'myapp/update_piglets.html', {
        'pig': pig,
        'form': form,
    })


# myapp/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Pig
from .forms import CheckHeatStatusForm

def check_heat_status(request, pig_id):
    pig = get_object_or_404(Pig, pig_id=pig_id)

    if request.method == "POST":
        form = CheckHeatStatusForm(request.POST)
        if form.is_valid():
            # รับข้อมูลจากฟอร์ม
            is_genital_swollen = form.cleaned_data['is_genital_swollen'] == 'yes'
            is_in_heat = form.cleaned_data['is_in_heat'] == 'yes'

            # อัปเดตสถานะของหมู
            pig.is_genital_swollen = is_genital_swollen
            pig.is_in_heat = is_in_heat
            pig.update_status()  # ใช้ฟังก์ชัน update_status เพื่อเปลี่ยนสถานะของหมู
            pig.save()

            return redirect('pig_list')  # ไปที่หน้า pig_list หลังจากอัปเดตสถานะ

    else:
        form = CheckHeatStatusForm()

    return render(request, 'myapp/check_heat_status.html', {'form': form, 'pig': pig})

def reset_mother_status(request, pig_id):
    pig = get_object_or_404(Pig, pig_id=pig_id)
    
    # รีเซ็ตสถานะเป็น "ยังไม่ผสม"
    pig.status = 'not_bred'
    pig.save()

    # ส่งข้อความแจ้งเตือนว่ารีเซ็ตสำเร็จ
    messages.success(request, f"หมู {pig.name} ถูกรีเซ็ตสถานะเป็น 'ยังไม่ผสม'")
    
    return redirect('breeding_history', pig_id=pig.pig_id)  # กลับไปที่หน้าประวัติการผสมของหมู

from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Pig, BreedingRecord

def export_pig(request, pig_id):
    pig = get_object_or_404(Pig, pig_id=pig_id)

    # ตรวจสอบสถานะหมู
    if pig.status == 'delivered':
        # เปลี่ยนสถานะหมูเป็น 'ยังไม่ผสม'
        pig.status = 'not_bred'
        pig.save()

        # บันทึกการส่งออกในประวัติการผสม
        BreedingRecord.objects.create(
            pig=pig,
            breeding_date=pig.breeding_records.latest('breeding_date').breeding_date,  # ใช้วันที่ผสมล่าสุด
            semen_id='ส่งออก',
            notes='ส่งออกลูกสุกรแล้ว'
        )

        # แสดงข้อความยืนยัน
        messages.success(request, f"หมู {pig.name} ถูกส่งออกและสถานะถูกรีเซ็ตเป็น 'ยังไม่ผสม'!")
    else:
        messages.error(request, "ไม่สามารถส่งออกหมูที่ไม่อยู่ในสถานะ 'คลอดแล้ว' ได้!")

    return redirect('breeding_history', pig_id=pig.pig_id)
