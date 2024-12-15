from django.contrib import admin
from django.urls import path, include  # รวม include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myapp.urls')),  # รวม urls ของ myapp
]

#---------------------------------------------------------