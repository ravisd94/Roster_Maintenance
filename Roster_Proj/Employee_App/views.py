from django.shortcuts import render
from .models import Emp_Master,Dept_Master,Designation_Master

# Create your views here.
def index(request):
    return render(request,'Pages\index.html')

def home(request):
    emps=Emp_Master.objects.all()
    context = {
        'page_title':'Home',
        'employees':emps,
        'total_department':len(Dept_Master.objects.all()),
        'total_position':len(Designation_Master.objects.all()),
        'total_employee':len(Emp_Master.objects.all()),
    }
    return render(request, 'Employee/Home.html',context)

def department(request):
    emps=Emp_Master.objects.all()
    context = {
        'page_title':'Home',
        'employees':emps,
        'total_department':len(Dept_Master.objects.all()),
        'total_position':len(Designation_Master.objects.all()),
        'total_employee':len(Emp_Master.objects.all()),
    }
    return render(request, 'Employee/Department.html',context)

def Manage_Employee(request):
    emps=Emp_Master.objects.all()
    context= {
    'emps':emps
    }
    print(context)
    return render(request,'Employee/Department.html',context)