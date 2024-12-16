from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

# URL patterns สำหรับแอปพลิเคชัน
urlpatterns = [
    path('', views.home, name='home'),  # เส้นทางไปยังหน้าแรก
    path('login/', views.custom_login, name='login'),  # เส้นทางสำหรับเข้าสู่ระบบ (custom login)
    path('register/', views.register, name='register'),  # เส้นทางสำหรับสมัครสมาชิก
    path('boss_dashboard/', views.boss_dashboard, name='boss_dashboard'),  # เส้นทางสำหรับแดชบอร์ดเจ้านาย
    path('employee_dashboard/', views.employee_dashboard, name='employee_dashboard'),  # เส้นทางสำหรับแดชบอร์ดพนักงาน
    path('search/', views.search_pigs, name='search_pigs'),
    path('insemination/<int:pig_id>/', views.insemination_record, name='insemination_record'),
    path('pig/<int:pig_id>/', views.pig_detail, name='pig_detail'),

    
]



