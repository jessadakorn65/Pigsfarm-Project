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
from django.contrib.auth.hashers import make_password

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # เข้ารหัสรหัสผ่าน
            user.secret_answer = make_password(form.cleaned_data['secret_answer'])  # เข้ารหัสคำตอบลับ
            user.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()

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


from django.shortcuts import render, get_object_or_404
from django.db.models import Sum
from .models import Pig, BreedingRecord

# ฟังก์ชันใน views.py ที่ใช้ในการสร้างข้อมูลกราฟ
def breeding_history(request, pig_id):
    pig = get_object_or_404(Pig, pig_id=pig_id)  # ใช้ pig_id เป็น primary key
    breeding_records = pig.breeding_records.all()  # ดึงข้อมูลประวัติการผสมทั้งหมดที่เชื่อมโยงกับหมูตัวนี้

    # ดึงบันทึกการคลอดล่าสุด
    latest_breeding_record = breeding_records.order_by('-delivery_date').first()

    # คำนวณจำนวนลูกสุกรที่รอดชีวิตจากแต่ละรหัสน้ำเชื้อ
    semen_stats = breeding_records.values('semen_id') \
                                   .annotate(total_alive_piglets=Sum('alive_piglets')) \
                                   .order_by('-total_alive_piglets')  # เรียงจากมากไปน้อย

    # กรองข้อมูลที่ไม่ต้องการ (กรองที่มีคำว่า "ส่งออก")
    semen_stats = semen_stats.exclude(semen_id='ส่งออก')

    # สร้างข้อมูลสำหรับกราฟ
    semen_ids = [stat['semen_id'] for stat in semen_stats]
    total_alive_piglets = [stat['total_alive_piglets'] for stat in semen_stats]

    return render(request, 'myapp/breeding_history.html', {
        'pig': pig,
        'breeding_records': breeding_records,
        'latest_breeding_record': latest_breeding_record,  # ส่งบันทึกการคลอดล่าสุด
        'semen_ids': semen_ids,  # ส่งข้อมูลรหัสน้ำเชื้อ
        'total_alive_piglets': total_alive_piglets  # ส่งข้อมูลจำนวนลูกสุกรที่รอดชีวิต
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
    latest_breeding_record = pig.breeding_records.order_by('-breeding_date').first()

    if not latest_breeding_record:
        messages.error(request, "ไม่พบประวัติการผสมสำหรับหมูตัวนี้")
        return redirect('breeding_history', pig_id=pig.pig_id)

    if request.method == "POST":
        form = PigletRecordForm(request.POST, instance=latest_breeding_record)
        if form.is_valid():
            form.save()
            pig.status = 'delivered'  # อัปเดตสถานะหมูเป็น "คลอดแล้ว"
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


import datetime
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import BreedingRecord, Pig

def export_pig(request, pig_id):
    pig = get_object_or_404(Pig, pig_id=pig_id)

    # ตรวจสอบสถานะหมู
    if pig.status == 'delivered':
        # เปลี่ยนสถานะหมูเป็น 'ยังไม่ผสม'
        pig.status = 'not_bred'
        pig.save()

        # บันทึกวันที่ส่งออก
        export_date = datetime.datetime.now()

        # ดึงเรคคอร์ดล่าสุดของหมู
        latest_record = pig.breeding_records.latest('breeding_date')

        # บันทึกการส่งออกในประวัติการผสม (ดึงแค่ "รอด" กับ "พิการ")
        BreedingRecord.objects.create(
        pig=pig,
        breeding_date=latest_record.breeding_date,
        semen_id='ส่งออก',
        alive_piglets=latest_record.alive_piglets,
        dead_piglets=latest_record.dead_piglets,  # ✅ เพิ่มเพื่อให้ total_piglets คำนวณถูกต้อง
        deformed_piglets=latest_record.deformed_piglets,
        notes=f'ส่งออกลูกสุกรเมื่อ {export_date.strftime("%Y-%m-%d %H:%M:%S")}',
        export_date=export_date
)


        # แสดงข้อความยืนยัน
        messages.success(request, f"หมู {pig.name} ถูกส่งออกและบันทึกวันที่ส่งออกเรียบร้อยแล้ว!")

    else:
        messages.error(request, "ไม่สามารถส่งออกหมูที่ไม่อยู่ในสถานะ 'คลอดแล้ว' ได้!")

    return redirect('breeding_history', pig_id=pig.pig_id)


from django.contrib import messages
from django.shortcuts import render

# ฟังก์ชันแสดงข้อความ
def some_view(request):
    # สร้างข้อความที่จะแสดงบนหน้าเว็บ
    messages.success(request, "การดำเนินการสำเร็จ!")  # หรือใช้ messages.warning, messages.error, etc.
    
    # เรนเดอร์กลับไปที่หน้า pig_queue หรือหน้าอื่น ๆ
    return render(request, 'myapp/pig_queue.html')



# --------------------------------dashboard --------------------------------
from django.shortcuts import render 
from django.db.models import Count, Sum
from .models import Pig, PigQueue, BreedingRecord
from django.db.models.functions import TruncMonth
import json
from datetime import date  # เพิ่มการใช้งาน date สำหรับการแสดงวันที่

from django.db.models import Sum, F

@login_required
def boss_dashboard(request):
    # ดึงจำนวนหมูทั้งหมด
    total_pigs = Pig.objects.count()

    # ดึงจำนวนหมูในแต่ละสถานะ
    pigs_not_bred = Pig.objects.filter(status='not_bred').count()
    pigs_ready = Pig.objects.filter(status='ready').count()
    pigs_bred = Pig.objects.filter(status='bred').count()
    pigs_delivered = Pig.objects.filter(status='delivered').count()

    # ดึงจำนวนหมูในคิว
    pigs_in_queue = PigQueue.objects.count()

    # นับจำนวนลูกสุกรที่รอดชีวิตจากการคลอด
    total_alive_piglets = BreedingRecord.objects.filter(pig__status='delivered').aggregate(total_alive=Sum('alive_piglets'))['total_alive'] or 0

    # นับจำนวนลูกสุกรที่ตาย
    total_dead_piglets = BreedingRecord.objects.filter(pig__status='delivered').aggregate(total_dead=Sum('dead_piglets'))['total_dead'] or 0

    # นับจำนวนลูกสุกรที่พิการ
    total_deformed_piglets = BreedingRecord.objects.filter(pig__status='delivered').aggregate(total_deformed=Sum('deformed_piglets'))['total_deformed'] or 0

    # คำนวณจำนวนลูกหมูที่คลอดจากแต่ละหมู
    pigs_delivery_stats = Pig.objects.filter(status='delivered')\
                                      .annotate(total_piglets=Sum('breeding_records__alive_piglets'))\
                                      .values('pig_id', 'total_piglets')

    # แปลงข้อมูลจำนวนลูกหมูที่คลอดเป็น JSON เพื่อใช้ในกราฟ
    pigs_delivery_stats_json = json.dumps(list(pigs_delivery_stats))

    # ดึงข้อมูลการผสมหมูในแต่ละเดือน
    breeding_stats = BreedingRecord.objects.annotate(month=TruncMonth('breeding_date')) \
                                           .values('month') \
                                           .annotate(count=Count('id')) \
                                           .order_by('month')

    # แปลงวันที่ใน `breeding_stats` ให้เป็นสตริงก่อนส่งไปยังเทมเพลต
    for stat in breeding_stats:
        stat['month'] = stat['month'].strftime('%Y-%m')

    # แปลงข้อมูลให้เป็น JSON
    breeding_stats_json = json.dumps(list(breeding_stats))

    # ดึงหมูที่มีสถานะ 'delivered' หรือ 'คลอดแล้ว'
    delivered_pigs = Pig.objects.filter(status='delivered')

    # ดึงประวัติแม่หมูที่คลอดลูก พร้อมจำนวนลูกสุกรที่รอด
    delivered_pigs_records = BreedingRecord.objects.filter(pig__status='delivered') \
        .values('pig__pig_id', 'pig__name', 'delivery_date') \
        .annotate(total_alive_piglets=Sum('alive_piglets')) \
        .order_by('-delivery_date')  # เรียงจากวันที่คลอดล่าสุด

    # ดึงข้อมูลของผู้ใช้และวันที่ปัจจุบัน
    today_date = date.today()
    user = request.user

    # ส่งข้อมูลไปที่เทมเพลต
    return render(request, 'myapp/boss_dashboard.html', {
        'total_pigs': total_pigs,
        'pigs_not_bred': pigs_not_bred,
        'pigs_ready': pigs_ready,
        'pigs_bred': pigs_bred,
        'pigs_delivered': pigs_delivered,
        'pigs_in_queue': pigs_in_queue,
        'total_alive_piglets': total_alive_piglets,
        'total_dead_piglets': total_dead_piglets,
        'total_deformed_piglets': total_deformed_piglets,
        'breeding_stats': breeding_stats_json,
        'delivered_pigs': delivered_pigs,  # ส่งหมูที่มีสถานะ 'delivered'
        'pigs_delivery_stats': pigs_delivery_stats_json,  # ส่งข้อมูลจำนวนลูกหมูที่คลอด
        'delivered_pigs_records': delivered_pigs_records,  # ส่งข้อมูลไปยังเทมเพลต
        'user': user,  # ส่งข้อมูลผู้ใช้ไปยังเทมเพลต
        'today_date': today_date,  # ส่งวันที่ปัจจุบันไปยังเทมเพลต
    })


from django.shortcuts import render, redirect
from .forms import CustomUserForm
from django.contrib.auth.decorators import login_required

@login_required
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        form = CustomUserForm(request.POST, request.FILES, instance=user)  # รับไฟล์รูปภาพด้วย
        if form.is_valid():
            form.save()
            return redirect('profile')  # ไปที่หน้าผู้ใช้หลังจากบันทึกสำเร็จ
    else:
        form = CustomUserForm(instance=user)  # แสดงฟอร์มการแก้ไข
    return render(request, 'myapp/edit_profile.html', {'form': form})

# views.py
@login_required
def profile(request):
    user = request.user  # ดึงข้อมูลผู้ใช้ที่ล็อกอินอยู่
    return render(request, 'myapp/profile.html', {'user': user})

# --------------------------------จบ------------------------------------------------
from django.shortcuts import render
from collections import defaultdict
from .models import BreedingRecord
from django.utils.dateformat import DateFormat

from django.utils.translation import gettext as _

def employee_dashboard(request):
    query = request.GET.get('q', '').strip()  # ค้นหาตาม pig_id
    month_filter = request.GET.get('month', '').strip()  # ค้นหาตามเดือน (1-12)

    records = BreedingRecord.objects.exclude(actual_date__isnull=True).order_by('actual_date')

    if query:
        records = records.filter(pig_id__icontains=query)  # ค้นหาตามรหัสแม่สุกร

    if month_filter:
        records = records.filter(actual_date__month=month_filter)  # ค้นหาตามเดือน

    grouped_records = defaultdict(list)

    for record in records:
        month_english = DateFormat(record.actual_date).format('F')  # "March"
        month_thai = {
            "January": "มกราคม", "February": "กุมภาพันธ์", "March": "มีนาคม",
            "April": "เมษายน", "May": "พฤษภาคม", "June": "มิถุนายน",
            "July": "กรกฎาคม", "August": "สิงหาคม", "September": "กันยายน",
            "October": "ตุลาคม", "November": "พฤศจิกายน", "December": "ธันวาคม"
        }.get(month_english, month_english)

        year = DateFormat(record.actual_date).format('Y')  # "2025"
        month_year = f"{month_thai} {year}"  # เช่น "มีนาคม 2025"

        total_piglets = record.alive_piglets + record.deformed_piglets

        grouped_records[month_year].append({
            'record': record,
            'total_piglets': total_piglets,
            'semen_id': record.semen_id
        })

    # ✅ เพิ่มตัวแปร months ที่ส่งไปยัง template
    months = [
        ('1', 'มกราคม'), ('2', 'กุมภาพันธ์'), ('3', 'มีนาคม'),
        ('4', 'เมษายน'), ('5', 'พฤษภาคม'), ('6', 'มิถุนายน'),
        ('7', 'กรกฎาคม'), ('8', 'สิงหาคม'), ('9', 'กันยายน'),
        ('10', 'ตุลาคม'), ('11', 'พฤศจิกายน'), ('12', 'ธันวาคม')
    ]

    context = {
        'grouped_records': dict(grouped_records),
        'query': query,
        'month_filter': month_filter,
        'months': months  # ✅ ส่งไปยัง template
    }

    return render(request, 'myapp/employee_dashboard.html', context)





from django.http import HttpResponse
from weasyprint import HTML
from django.template.loader import render_to_string
from collections import defaultdict
from django.utils.dateformat import DateFormat
from myapp.models import BreedingRecord  # นำเข้าโมเดล BreedingRecord

def download_pdf(request):
    records = BreedingRecord.objects.exclude(actual_date__isnull=True).order_by('actual_date')

    grouped_records = defaultdict(list)

    for record in records:
        month_english = DateFormat(record.actual_date).format('F')  # "March"
        month_thai = {
            "January": "มกราคม", "February": "กุมภาพันธ์", "March": "มีนาคม",
            "April": "เมษายน", "May": "พฤษภาคม", "June": "มิถุนายน",
            "July": "กรกฎาคม", "August": "สิงหาคม", "September": "กันยายน",
            "October": "ตุลาคม", "November": "พฤศจิกายน", "December": "ธันวาคม"
        }.get(month_english, month_english)

        year = DateFormat(record.actual_date).format('Y')  # "2025"
        month_year = f"{month_thai} {year}"  # เช่น "มีนาคม 2025"

        total_piglets = record.alive_piglets + record.deformed_piglets

        # เพิ่มเงื่อนไขให้ตรงกับ employee_dashboard
        if total_piglets > 0 and record.semen_id != "ส่งออก":
            grouped_records[month_year].append({
                'record': record,
                'total_piglets': total_piglets,
                'semen_id': record.semen_id
            })

    context = {
        'grouped_records': dict(grouped_records),
    }

    html_string = render_to_string('myapp/pdf_template.html', context)
    pdf_file = HTML(string=html_string).write_pdf()

    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    return response

from django.shortcuts import render

# ฟังก์ชันสำหรับหน้า Dashboard
def dashboard(request):
    # ถ้าต้องการข้อมูลเพิ่มเติมสามารถส่งไปยังหน้า HTML ได้ที่นี่
    return render(request, 'myapp/dashboard.html')

from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password, make_password
from .models import CustomUser
from .forms import PasswordResetForm

def password_reset(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            secret_answer = form.cleaned_data["secret_answer"]
            new_password = form.cleaned_data["new_password"]

            try:
                user = CustomUser.objects.get(username=username)
                if user.secret_answer and check_password(secret_answer, user.secret_answer):  
                    user.password = make_password(new_password)  # ตั้งรหัสผ่านใหม่
                    user.save()
                    return redirect("login")  # ส่งผู้ใช้ไปยังหน้าเข้าสู่ระบบหลังจากรีเซ็ตรหัสผ่านสำเร็จ
                else:
                    form.add_error(None, "Secret answer is incorrect.")
            except CustomUser.DoesNotExist:
                form.add_error("username", "Username not found.")

    else:
        form = PasswordResetForm()

    return render(request, "myapp/password_reset.html", {"form": form})
