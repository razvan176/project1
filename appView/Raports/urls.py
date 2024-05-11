from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('raport/',views.index),
    path('vmtas/',views.vmtas),
    path('sent_test/',views.send_test),

    path('vmtas/getVmtas/', views.getVmtas, name='get_vmtas'),
    path('vmtas/getVmtaLog/', views.getVmtaLog, name='get_vmta_log'),
    path('vmtas/saveVmtaLog/', views.saveVmtaLog, name='save_vmta_log'),
]

