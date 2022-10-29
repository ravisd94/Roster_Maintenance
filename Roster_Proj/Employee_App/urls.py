from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    # Department Urls
    path('department', views.department, name="department"),
    # path('department/validate', views.validate_dept, name="validate_dept"),
    path('department/manage', views.manage_dept, name="department/manage"),
    path('department/delete', views.delete_dept, name="department/delete"),
    path('department/save_department', views.save_department,name="save_department"),

    # End Department Urls

    # Designation Urls
    path('designation', views.designation, name="designation"),
    path('designation/manage', views.manage_desg, name="designation/manage"),
    path('designation/delete', views.delete_desg, name="designation/delete"),
    path('designation/save_designation', views.save_designation),
    # # End Designation Urls

    # # Role Urls
    path('role', views.role, name="role"),
    path('role/manage', views.manage_role, name="role/manage"),
    path('role/delete', views.delete_role, name="role/delete"),
    path('role/save_role', views.save_role),
    # # End Role Urls

    # # Role Urls
    path('employee', views.employee, name="employee"),
    path('employee/manage', views.manage_emp, name="employee/manage"),
    path('employee/delete', views.delete_emp, name="employee/delete"),
    path('employee/save_emp', views.save_emp,name="save_emp"),
    # # End Role Urls
]