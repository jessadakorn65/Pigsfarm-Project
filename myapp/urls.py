from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
# URL patterns สำหรับแอปพลิเคชัน
urlpatterns = [
    path('', views.home, name='home'),  # เส้นทางไปยังหน้าแรก
    path('login/', views.custom_login, name='login'),  # เส้นทางสำหรับเข้าสู่ระบบ (custom login)
    path('register/', views.register, name='register'),  # เส้นทางสำหรับสมัครสมาชิก
    path('boss_dashboard/', views.boss_dashboard, name='boss_dashboard'),  # เส้นทางสำหรับแดชบอร์ดเจ้านาย
    path('employee_dashboard/', views.employee_dashboard, name='employee_dashboard'),  # เส้นทางสำหรับแดชบอร์ดพนักงาน
    path('pigs/', views.pig_list, name='pig_list'),
    path('add_pig/', views.add_pig, name='add_pig'),
    path('pigs/<str:pig_id>/edit/', views.edit_pig, name='edit_pig'),
    path('pigs/<str:pig_id>/delete/', views.delete_pig, name='delete_pig'),
    path('pigs/<str:pig_id>/record/', views.record_breeding, name='record_breeding'),
    path('<str:pig_id>/breeding_history/', views.breeding_history, name='breeding_history'),
    path('delete_breeding_record/<int:record_id>/', views.delete_breeding_record, name='delete_breeding_record'),

   
    path('queue/', views.pig_queue, name='pig_queue'),
    path('queue/add/<str:pig_id>/', views.add_to_queue, name='add_to_queue'),
    path('queue/remove/<int:queue_id>/', views.remove_from_queue, name='remove_from_queue'),
  
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
