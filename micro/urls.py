from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('login/', views.log_in,name='login'),
    path('register/',views.register, name='register'),
    path('logout/', views.log_out, name='logout'),
    path('save/', views.save_pic, name='save'),
    path('sequential/', views.sequential, name='sequential'),
    path('comparison/', views.comparison, name='comparison')
]