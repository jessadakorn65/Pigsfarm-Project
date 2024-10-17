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
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]
