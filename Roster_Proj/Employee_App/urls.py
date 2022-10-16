from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('department', views.department, name="department"),
    # path('', views.index,name='Pages/index.html'),
    # path('Manage_Employee', views.Manage_Employee,name='Manage_Employee.html'),
]