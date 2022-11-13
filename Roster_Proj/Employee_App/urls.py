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
    path('designation/save_designation', views.save_designation,name="save_designation"),
    # # End Designation Urls

    # # Role Urls
    path('role', views.role, name="role"),
    path('role/manage', views.manage_role, name="role/manage"),
    path('role/delete', views.delete_role, name="role/delete"),
    path('role/save_role', views.save_role,name="save_role"),
    # # End Role Urls

    # # Project Urls
    path('project', views.project, name="project"),
    path('project/manage', views.manage_project, name="project/manage"),
    path('project/delete', views.delete_project, name="project/delete"),
    path('project/save_project', views.save_project,name="save_project"),
    # # End Project Urls

    # # Employee Urls
    path('employee', views.employee, name="employee"),
    path('employee/manage', views.manage_emp, name="employee/manage"),
    path('employee/delete', views.delete_emp, name="employee/delete"),
    path('employee/save_emp', views.save_emp,name="save_emp"),
    # # End Employee Urls

    # # Shift Urls
    # Shift Management
    path('shift', views.shift, name="shift"),
    path('shift/manage', views.manage_shift, name="shift/manage"),
    path('shift/delete', views.delete_shift, name="shift/delete"),
    path('shift/save_shift', views.save_shift,name="save_shift"),
    # End Shift Management
    
    # Shift Assignment
    path('shift/assign', views.assign_shift, name="assign_shift"),
    path('shift/assign/manage', views.manage_assign_shift, name="shift/assign/manage"),
    path('shift/assign/delete', views.delete_assign_shift, name="shift/assign/delete"),
    path('shift/assign/save_assign_shift', views.save_assign_shift, name="save_assign_shift"),
    # End Shift Assignment

    # Shift Calender
    path('shift/calender', views.shift_calender, name="shift_calender"),
    path('Get_Assigned_Shifts', views.Get_Assigned_Shifts, name="Get_Assigned_Shifts"),
    # End Shift Calender

    # # End Shift Urls
    # Attendance
    path('attendance/timesheet', views.timesheet, name="timesheet"),
    path('attendance/mark_attendance', views.mark_attendance, name="mark_attendance"),
    path('Get_Shift_Details', views.Get_Shift_Details, name="Get_Shift_Details"),
    path('attendance/Clock_In_Clock_Out', views.Clock_In_Clock_Out, name="Clock_In_Clock_Out"),
    path('attendance/calender', views.attendance_calender, name="attendance_calender"),
    path('Get_Calender_Details', views.Get_Calender_Details, name="Get_Calender_Details"),
    
    # End Attendance
]