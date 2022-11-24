from django.contrib import admin
from Employee_App.models import Dept_Master
from Employee_App.models import Designation_Master
from Employee_App.models import Role_Master
from Employee_App.models import Project_Master
from Employee_App.models import Emp_Master
from Employee_App.models import Shift_Master
from Employee_App.models import Employee_Shift_Master
from Employee_App.models import Attendance_Type
from Employee_App.models import Attendance_Master

# Register your models here.

admin.site.register(Dept_Master)
admin.site.register(Designation_Master)
admin.site.register(Role_Master)
admin.site.register(Project_Master)
admin.site.register(Emp_Master)
admin.site.register(Shift_Master)
admin.site.register(Employee_Shift_Master)
admin.site.register(Attendance_Type)
admin.site.register(Attendance_Master)