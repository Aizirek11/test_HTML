from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

# Главная страница прямо через функцию
def home(request):
    return HttpResponse("Hello, world! Django is running ✅")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),  # главная страница /
    path('men/', include('men.urls')),  # остальные URL приложения men
]

