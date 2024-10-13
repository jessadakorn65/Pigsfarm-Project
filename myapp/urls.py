from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.custom_login, name='login'),  # เปลี่ยนจาก login_view เป็น custom_login
    path('register/', views.register, name='register'),
    path('boss_dashboard/', views.boss_dashboard, name='boss_dashboard'),
    path('employee_dashboard/', views.employee_dashboard, name='employee_dashboard'),
    path('register/', views.register, name='register'),  # ตัวอย่างการกำหนดชื่อ URL
]
