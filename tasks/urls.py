from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/add-task/', views.trigger_add_task, name='trigger_add_task'),
    path('api/email-task/', views.trigger_email_task, name='trigger_email_task'),
    path('api/process-task/', views.trigger_process_task, name='trigger_process_task'),
]

