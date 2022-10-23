from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('test', views.test,name="test"),
    path('department', views.department, name="department"),
    path('department/add', views.add_department, name="department/add"),
    path('department/manage', views.manage_dept, name="department/manage"),
    path('department/delete', views.delete_dept, name="department/delete"),
    path('department/save_department', views.save_department),
    path('delete_department', views.delete_department, name="delete-department"),
    # path('', views.index,name='Pages/index.html'),
    # path('Manage_Employee', views.Manage_Employee,name='Manage_Employee.html'),
]