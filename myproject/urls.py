from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myapp.urls')),  # รวม urls ของ myapp
]


# เพิ่มการเสิร์ฟไฟล์มีเดียในโหมด Debug
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#---------------------------------------------------------