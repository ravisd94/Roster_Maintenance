from django.shortcuts import render
from .models import Emp_Master,Dept_Master,Designation_Master
from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
import json
from django.contrib import messages #import messages

# Create your views here.
def index(request):
    return render(request,'Pages\index.html')

def test(request):
    return render(request,'Pages\\test.html')

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

# Department Views
def department(request):
    department_list = Dept_Master.objects.all()
    msg=''
    if 'msg' in request.session:
        msg=request.session['msg']
    print(msg)
    context = {
        'page_title':'Departments',
        'departments':department_list,
        'msg':msg
    }
    return render(request, 'Employee/Department/Departments.html',context)

def add_department(request):
    context = {
        'page_title':'Add the Department',

    }
    return render(request, 'Employee/Department/add.html',context)

def manage_dept(request):
    is_New = True
    card_header=''
    department = {}
    data =  request.GET
    id = ''
    if 'id' in data:
        id = data['id']
    if id == '':
        card_header='Create New '
    else:
        department = Dept_Master.objects.filter(Dept_Id=id).first()
        card_header='Edit '
    context = {
        'department' : department,
        'card_header': card_header
    }
    return render(request, 'Employee/Department/manage_department.html',context)

def delete_dept(request):
    id = request.GET['id']
    Dept_Master.objects.filter(Dept_Id = id).delete()
    return HttpResponseRedirect("/department")

def save_department(request):
    if request.method == 'POST':
        data =  request.POST

        for key, value in request.POST.items():
            print('Key: %s' % (key) ) 
            print('Value %s' % (value) )

        Name = data['Dept_Name']
        Desc = data['Dept_description']
        print("Desc"+Desc)
        Status = data['Dept_Status']
        if Status == 'on':
            Status=True
        else:
            Status=False
        print("status: "+str(Status))
        try:
            id  = ''
            if 'id' in data:
                id = data['id']
            if id == '':
                save_department = Dept_Master(Dept_Name=Name, Dept_description = Desc,Dept_Status = Status)
                save_department.save()
                request.session['msg']="Department added successfully"
                messages.SUCCESS(request, "Department added successfully")
            else:
                Dept_Master.objects.filter(Dept_Id = id).update(Dept_Name = Name,Dept_Status=Status,Dept_Description = Desc)
                request.session['msg']="Department id: "+ id +" edited successfully"
            
        except Exception as e:
            messages.error(request,"Somehing went wrong!, please contact to system administrator..." + str(type(e)))
            print(type(e))
        return HttpResponseRedirect("/department")
        # return department()
        # return render(request,'Employee/Department/Departments.html',{'msg':msg})
    # return HttpResponse(json.dumps(resp), content_type="application/json")
    else:
        return HttpResponse("<h1>404 - Page not found...")

def delete_department(request):
    data =  request.POST
    resp = {'status':''}
    try:
        Dept_Master.objects.filter(id = data['id']).delete()
        resp['status'] = 'success'
    except:
        resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")

# End Department Views

def Manage_Employee(request):
    emps=Emp_Master.objects.all()
    context= {
    'emps':emps
    }
    print(context)
    return render(request,'Employee/Department.html',context)