import datetime
from msilib.schema import _Validation
from urllib import response
from xml.dom import ValidationErr
from django.shortcuts import render
from .models import Emp_Master,Dept_Master,Designation_Master, Role_Master, Shift_Master, Employee_Shift_Master,Attendance_Master, Attendance_Type, Project_Master
from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
import json
from django.contrib import messages #import messages
from django import forms
from .forms import RoleForm_Add
import re
import random
from datetime import timedelta
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
import manage 
from django.http import HttpResponse

import qrcode
from django.http import HttpResponse
from django.utils.text import slugify


# Create your views here.
def user_login(request):
    if request.method == 'POST':
        data =  request.POST
        email = data['email']
        password = data['password']

        # user2 = Emp_Master.objects.get(Emp_Id = 3)
        # user2.set_password('test')
        # user2.save()

        user = authenticate(request,email = 'ravi@test.com', password= "test")
        user1 = Emp_Master.objects.filter(Emp_Id = '2').first()
        if user is None:
            print('Invalid Credentials')
            return render(request,'Accounts/login.html')
        else:
            login(request,user)
            request.session['user_email']= user.email
            request.session['user_Emp_Id']= user.Emp_Id
            request.session['user_is_superuser']= user.is_superuser
            request.session['user_is_ProjectManager_or_SuperAdmin'] = True if user.Role_Id.Role_Name == 'Project Manager' or user.is_superuser == True else False
            request.session['user_fullName']= user.first_name + " " + user.Middle_Name + " " + user.last_name
            request.session['user_last_login']= user.last_login.strftime("%d-%b-%y %I:%M %p")
            request.session['user_Gender']= user.Emp_Sex
            pswd = Emp_Master.objects.make_random_password(length=14)
            print(request.session['user_is_ProjectManager_or_SuperAdmin'])
            subject = "Id creation in Roster Mangement"  
            msg = f"""
                Dear Ravi Sakharam Dhondkar,
                Your id has been created in Roster Mangement, please use below password to login.
                Password: {pswd}."""
            from_id = "info@lbmrecruitment.com.au"
            to = ['ravi.dhondkar@gmail.com']
            # res     = send_mail(subject, msg, from_id, ['ravi.dhondkar@gmail.com'] )  
            # if(res == 1):  
            #     msg = "Mail Sent Successfuly"  
            # else:  
            #     msg = "Mail could not sent"  


            if request.GET.get('next',None):
                print(request.GET['next'])
                return HttpResponseRedirect(request.GET['next'])
            return HttpResponseRedirect("/")
    return render(request,'Accounts/login.html')
    # u = Emp_Master.objects.get(Emp_Id=1)
    # u.set_password('Codestack@123')
    # u.save()

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('login')

@login_required(login_url='/accounts/login')
def home(request):
    emps=Emp_Master.objects.all()
    attendance_list_today = Attendance_Master.objects.filter(Attendance_Date=datetime.date.today())
    context = {
        'page_title':'Home',
        'employees':emps,
        'total_department':len(Dept_Master.objects.all()),
        'total_position':len(Designation_Master.objects.all()),
        'total_employee':len(Emp_Master.objects.all()),
        'total_Present': len(attendance_list_today)
    }
    return render(request, 'Employee/Home.html',context)

# Department Views.
@login_required(login_url='/accounts/login')
def department(request):
    department_list = Dept_Master.objects.all()
    context = {
        'page_title':'Departments',
        'departments':department_list,
    }
    return render(request, 'Employee/Department/Departments.html',context)

@login_required(login_url='/accounts/login')
def manage_dept(request):
    card_header=''
    department = {}
    data =  request.GET
    id = ''
    details=''
    if 'id' in data:
        id = data['id']
        if id != '':
            department = Dept_Master.objects.filter(Dept_Id=id).first()
        card_header='Edit the Department'

    if 'details' in data:
        details = data['details']
        if details != '':
            department = Dept_Master.objects.filter(Dept_Id=details).first()
            card_header='Details of Department: ' + department.Dept_Name
    
    if 'id' not in data and 'details' not in data:
        card_header='Create New Department'

    context = {
        'department' : department,
        'card_header': card_header,
        'details' : details
    }
    return render(request, 'Employee/Department/manage_department.html',context)

@login_required(login_url='/accounts/login')
def delete_dept(request):
    try:
        id = request.GET['id']
        Dept_Master.objects.filter(Dept_Id = id).delete()
        messages.warning(request, "Department id: "+str(id)+" Deleted successfully")
    except Exception as e:
        messages.error(request,"Somehing went wrong!, please contact to system administrator...")
    return HttpResponseRedirect("/department")

@login_required(login_url='/accounts/login')
def save_department(request):
    if request.method == 'POST':
        data =  request.POST
        Status=''
        resp = {'status':'failed', 'msg': ''}
        print("------------------All Key value Pairs-------------")
        for key, value in data.items():
            print('Key: %s' % (key) ) 
            print('Value %s' % (value) )
        print("------------------End All Key value Pairs-------------")
        Name = data['Dept_Name']
        Desc = data['Dept_description']
        print(Name)
        print(Desc)
        isExist = Dept_Master.isExists(Name)
        print(isExist)

        if 'Dept_Status' in data:
            Status = data['Dept_Status']
            if Status == 'on':
                Status=True
        else:
            Status=False
        print("status: "+ str(Status))
        try:
            ret = HttpResponse(json.dumps(resp), content_type="application/json")
            id  = ''
            if 'Dept_Id' in data:
                id = data['Dept_Id']
            print('id:'+id)
            # print('test: ' not isExist)
            if id == '':
                if Name is None:
                    resp['status'] = 'failed'
                    resp['msg']= "Name is mandatory, please add Name"
                    print(str(resp['msg']))
                    return HttpResponse(json.dumps(resp), content_type="application/json")
                
                if isExist == True:
                    resp['status'] = 'failed'
                    resp['msg']="Department '"+Name+"' is already exist, please use other name"
                    print(str(resp['msg']))
                    # messages.error(request, "Department '"+Name+"' is already exist, please use other name")
                    return HttpResponse(json.dumps(resp), content_type="application/json")
                
                save_department = Dept_Master(Dept_Name=Name, Dept_description = Desc,Dept_Status = True)
                save_department.save()
                messages.success(request, "Department added successfully")   
                resp['status'] = 'success'
                return HttpResponse(json.dumps(resp), content_type="application/json")   
                # return HttpResponseRedirect('/department')  
                    
            else:
                print("Now: "+str(datetime.datetime.now()))
                Dept_Master.objects.filter(Dept_Id = id).update(
                    Dept_Name = Name,
                    Dept_Status=Status,
                    Dept_description = Desc, 
                    Modified_Date = datetime.datetime.now()  )
                resp['status'] = 'success'
                messages.success(request, "Department id: "+str(id)+" updated successfully")  
                print(str(resp['msg']))
                # return HttpResponseRedirect('/department')
                return HttpResponse(json.dumps(resp), content_type="application/json")   
                # return department(request)
            
        except Exception as e:
            resp['status'] = 'failed'
            resp['msg']="Somehing went wrong!, please contact to system administrator..." + str(type(e))
            print(str(resp['msg']))
            return HttpResponse(json.dumps(resp), content_type="application/json")
        print('final')
        return HttpResponseRedirect("/department")
        # return department()
        # return render(request,'Employee/Department/Departments.html',{'msg':msg})
    # return HttpResponse(json.dumps(resp), content_type="application/json")
    else:
        return HttpResponse("<h1>404 - Page not found...")

# End Department Views

# Designation Views
@login_required(login_url='/accounts/login')
def designation(request):
    designation_list = Designation_Master.objects.all()
    context = {
        'page_title':'Designation',
        'designations':designation_list,
    }
    return render(request, 'Employee/Designation/Designations.html',context)

@login_required(login_url='/accounts/login')
def manage_desg(request):
    card_header=''
    designation = {}
    Dept_Active_List = Dept_Master.objects.filter(Dept_Status=True).all()
    data =  request.GET
    id = ''
    details=''
    if 'id' not in data and 'details' not in data:
        card_header='Create New Designation'
    else:
        if 'id' in data:
            id = data['id']
            if id != '':
                designation = Designation_Master.objects.filter(Desg_Id=id).first()
            card_header='Edit the Designation'

        if 'details' in data:
            details = data['details']
            if details != '':
                designation = Designation_Master.objects.filter(Desg_Id=details).first()
                card_header='Details of Designation: ' + designation.Desg_Name
    #print(designation.Dept_Id)
    context = {
        'designation' : designation,
        'departments' : Dept_Active_List,
        'card_header': card_header,
        'details' : details
    }
    return render(request, 'Employee/Designation/manage_designation.html',context)

@login_required(login_url='/accounts/login')
def save_designation(request):
    if request.method == 'POST':
        data =  request.POST
        Status=''
        resp = {'status':'failed', 'msg': ''}
        print("------------------All Key value Pairs-------------")
        for key, value in data.items():
            print('Key: %s' % (key) ) 
            print('Value %s' % (value) )
        print("------------------End All Key value Pairs-------------")
        Name = data['Desg_Name']
        Desc = data['Desg_description']
        print(Name)
        print(Desc)
        isExist = Designation_Master.isExists(Name)
        print(isExist)

        if 'Desg_Status' in data:
            Status = data['Desg_Status']
            if Status == 'on':
                Status=True
        else:
            Status=False
        print("status: "+ str(Status))
        try:
            ret = HttpResponse(json.dumps(resp), content_type="application/json")
            id  = ''
            Dept_Id=''
            if 'Desg_Id' in data:
                id = data['Desg_Id']
            print('id:'+id)
            
            if 'Dept_Id' in data:
                Dept_Id = Dept_Master.objects.filter(Dept_Id =  data['Dept_Id']).first()
            print('Dept_Id: '+ str(Dept_Id))
            # print('test: ' not isExist)
            if id == '':
                if Name is None:
                    resp['status'] = 'failed'
                    resp['msg']= "Name is mandatory, please add Name"
                    print(str(resp['msg']))
                    return HttpResponse(json.dumps(resp), content_type="application/json")
                
                if isExist == True:
                    resp['status'] = 'failed'
                    resp['msg']="Department '"+Name+"' is already exist, please use other name"
                    print(str(resp['msg']))
                    # messages.error(request, "Department '"+Name+"' is already exist, please use other name")
                    return HttpResponse(json.dumps(resp), content_type="application/json")
                
                save_designation = Designation_Master(
                    Dept_Id=Dept_Id,
                    Desg_Name=Name, 
                    Desg_description = Desc,
                    Desg_Status = True
                    )
                save_designation.save()
                messages.success(request, "Designation added successfully")   
                resp['status'] = 'success'
                return HttpResponse(json.dumps(resp), content_type="application/json")   
                # return HttpResponseRedirect('/department')  
                    
            else:
                print("Now: "+str(datetime.datetime.now()))
                Designation_Master.objects.filter(Desg_Id = id).update(
                    Dept_Id=Dept_Id,
                    Desg_Name = Name,
                    Desg_Status=Status,
                    Desg_description = Desc, 
                    Modified_Date = datetime.datetime.now()  )
                resp['status'] = 'success'
                messages.success(request, "Designation id: "+str(id)+" updated successfully")  
                print(str(resp['msg']))
                # return HttpResponseRedirect('/department')
                return HttpResponse(json.dumps(resp), content_type="application/json")   
                # return department(request)
            
        except Exception as e:
            resp['status'] = 'failed'
            resp['msg']="Somehing went wrong!, please contact to system administrator..." + str(e)
            print(str(resp['msg']))
            return HttpResponse(json.dumps(resp), content_type="application/json")
        print('final')
        return HttpResponseRedirect("/designation")
        # return department()
        # return render(request,'Employee/Department/Departments.html',{'msg':msg})
    # return HttpResponse(json.dumps(resp), content_type="application/json")
    else:
        return HttpResponse("<h1>404 - Page not found...")

@login_required(login_url='/accounts/login')
def delete_desg(request):
    try:
        id = request.GET['id']
        Designation_Master.objects.filter(Desg_Id = id).delete()
        messages.warning(request, "Designation id: "+str(id)+" Deleted successfully")
    except Exception as e:
        messages.error(request,"Somehing went wrong!, please contact to system administrator...")
    return HttpResponseRedirect("/designation")

# End Designation Views

# Role Views
@login_required(login_url='/accounts/login')
def role(request):
    role_list = Role_Master.objects.all()
    context = {
        'page_title':'Role',
        'roles':role_list,
    }
    return render(request, 'Employee/Role/Roles.html',context)

@login_required(login_url='/accounts/login')
def manage_role(request):
    card_header=''
    role = {}
    data =  request.GET
    id = ''
    details=''
    if 'id' in data:
        id = data['id']
        if id != '':
            role = Role_Master.objects.filter(Role_Id=id).first()
        card_header='Edit the Role'

    if 'details' in data:
        details = data['details']
        if details != '':
            role = Role_Master.objects.filter(Role_Id=details).first()
            card_header='Details of Role: ' + role.Role_Name
    
    if 'id' not in data and 'details' not in data:
        card_header='Create New Role'

    context = {
        'role' : role,
        'card_header': card_header,
        'details' : details
    }
    return render(request, 'Employee/Role/manage_role.html',context)

@login_required(login_url='/accounts/login')
def save_role(request):
    if request.method == 'POST':
        data =  request.POST
        Status=''
        resp = {'status':'failed', 'msg': ''}
        print("------------------All Key value Pairs-------------")
        for key, value in data.items():
            print('Key: %s' % (key) ) 
            print('Value %s' % (value) )
        print("------------------End All Key value Pairs-------------")
        Name = data['Role_Name']
        Desc = data['Role_description']
        print(Name)
        print(Desc)
        isExist = Role_Master.isExists(Name)
        print(isExist)

        if 'Role_Status' in data:
            Status = data['Role_Status']
            if Status == 'on':
                Status=True
        else:
            Status=False
        print("status: "+ str(Status))
        try:
            ret = HttpResponse(json.dumps(resp), content_type="application/json")
            id  = ''
            if 'Role_Id' in data:
                id = data['Role_Id']
            print('id:'+id)
            # print('test: ' not isExist)
            if id == '':
                if Name is None:
                    resp['status'] = 'failed'
                    resp['msg']= "Name is mandatory, please add Name"
                    print(str(resp['msg']))
                    return HttpResponse(json.dumps(resp), content_type="application/json")
                
                if isExist == True:
                    resp['status'] = 'failed'
                    resp['msg']="Department '"+Name+"' is already exist, please use other name"
                    print(str(resp['msg']))
                    # messages.error(request, "Department '"+Name+"' is already exist, please use other name")
                    return HttpResponse(json.dumps(resp), content_type="application/json")
                
                save_role = Role_Master(Role_Name=Name, Role_description = Desc,Role_Status = True)
                save_role.save()
                messages.success(request, "Role added successfully")   
                resp['status'] = 'success'
                return HttpResponse(json.dumps(resp), content_type="application/json")   
                # return HttpResponseRedirect('/department')  
                    
            else:
                print("Now: "+str(datetime.datetime.now()))
                Role_Master.objects.filter(Role_Id = id).update(
                    Role_Name = Name,
                    Role_Status=Status,
                    Role_description = Desc, 
                    Modified_Date = datetime.datetime.now()  )
                resp['status'] = 'success'
                messages.success(request, "Role id: "+str(id)+" updated successfully")  
                print(str(resp['msg']))
                return HttpResponse(json.dumps(resp), content_type="application/json")   
            
        except Exception as e:
            resp['status'] = 'failed'
            resp['msg']="Somehing went wrong!, please contact to system administrator..." + str(type(e))
            print(str(resp['msg']))
            return HttpResponse(json.dumps(resp), content_type="application/json")
        print('final')
        return HttpResponseRedirect("/department")

    else:
        return HttpResponse("<h1>404 - Page not found...")

@login_required(login_url='/accounts/login')
def delete_role(request):
    try:
        id = request.GET['id']
        Role_Master.objects.filter(Role_Id = id).delete()
        messages.warning(request, "Role id: "+str(id)+" Deleted successfully")
    except Exception as e:
        messages.error(request,"Somehing went wrong!, please contact to system administrator...")
    return HttpResponseRedirect("/role")

# End Role Views

# Employee Views

# Project Views
@login_required(login_url='/accounts/login')
def project(request):
    project_list = Project_Master.objects.all()
    for project in project_list:
        print('Key: %s:' + str(project.Proj_Name) )
    context = {
        'page_title':'Project',
        'projects':project_list,
    }
    return render(request, 'Employee/Project/Projects.html',context)

@login_required(login_url='/accounts/login')
def manage_project(request):
    card_header=''
    project = {}
    data =  request.GET
    id = ''
    details=''
    for key, value in data.items():
            print('Key: %s' % (key) ) 
            print('Value %s' % (value) )
            
    if 'id' in data:
        id = data['id']
        if id != '':
            project = Project_Master.objects.filter(Proj_id=id).first()
        card_header='Edit the Project'

    if 'details' in data:
        details = data['details']
        if details != '':
            project = Project_Master.objects.filter(Proj_id=details).first()
            card_header='Details of Project: ' + project.Proj_Name
    
    if 'id' not in data and 'details' not in data:
        card_header='Create New Project'

    context = {
        'project' : project,
        'card_header': card_header,
        'details' : details
    }
    return render(request, 'Employee/Project/manage_project.html',context)

@login_required(login_url='/accounts/login')
def save_project(request):
    if request.method == 'POST':
        data =  request.POST
        Status=''
        resp = {'status':'failed', 'msg': ''}
        print("------------------All Key value Pairs-------------")
        for key, value in data.items():
            print('Key: %s' % (key) ) 
            print('Value %s' % (value) )
        print("------------------End All Key value Pairs-------------")
        
        Proj_Name = data['Proj_Name']
        Proj_Description = data['Proj_Description']
        Client_Name = data['Client_Name']
        Point_of_Contact_Name = data['Point_of_Contact_Name']
        Point_of_Contact_Email = data['Point_of_Contact_Email']
        Proj_Start_Date = data['Proj_Start_Date']
        Proj_End_Date = data['Proj_End_Date']

        isExist = Project_Master.isExists(Proj_Name)
        print(isExist)

        if 'Proj_Status' in data:
            Status = data['Proj_Status']
            if Status == 'on':
                Status=True
        else:
            Status=False
        print("status: "+ str(Status))
        try:
            ret = HttpResponse(json.dumps(resp), content_type="application/json")
            id  = ''
            if 'Proj_id' in data:
                id = data['Proj_id']
            print('id:'+id)
            # print('test: ' not isExist)
            if id == '':
                if Proj_Name is None:
                    resp['status'] = 'failed'
                    resp['msg']= "Project Name is mandatory, please add Name"
                    print(str(resp['msg']))
                    return HttpResponse(json.dumps(resp), content_type="application/json")
                
                if isExist == True:
                    resp['status'] = 'failed'
                    resp['msg']="Project Name '"+Proj_Name+"' is already exist, please use other name"
                    print(str(resp['msg']))
                    # messages.error(request, "Department '"+Name+"' is already exist, please use other name")
                    return HttpResponse(json.dumps(resp), content_type="application/json")
                
                # qrcode_img = qrcode.make(Proj_Name)
                # canvas = Image.new('RGB',(290,290),'white')
                # draw = ImageDraw.Draw(canvas)
                # canvas.paste(qrcode_img)
                # buffer = BytesIO()
                # canvas.save(buffer,'PNG')

                save_project = Project_Master.objects.create(Proj_Name=Proj_Name, Proj_Description = Proj_Description,Proj_Status = True,
                    Client_Name=Client_Name,Point_of_Contact_Name=Point_of_Contact_Name,
                    Point_of_Contact_Email=Point_of_Contact_Email,Proj_Start_Date=Proj_Start_Date, Proj_End_Date=Proj_End_Date
                    )
                
                save_project.save()
                messages.success(request, "Project added successfully")   
                resp['status'] = 'success'
                return HttpResponse(json.dumps(resp), content_type="application/json")   
                # return HttpResponseRedirect('/department')  
                    
            else:
                print("Now: "+str(datetime.datetime.now()))
                Project_Master.objects.filter(Proj_id = id).update(
                    Proj_Name=Proj_Name, Proj_Description = Proj_Description,Proj_Status = Status,
                    Client_Name=Client_Name,Point_of_Contact_Name=Point_of_Contact_Name,
                    Point_of_Contact_Email=Point_of_Contact_Email,Proj_Start_Date=Proj_Start_Date, Proj_End_Date=Proj_End_Date,
                    Modified_Date = datetime.datetime.now()  )
                resp['status'] = 'success'
                messages.success(request, "Role id: "+str(id)+" updated successfully")  
                print(str(resp['msg']))
                return HttpResponse(json.dumps(resp), content_type="application/json")   
            
        except Exception as e:
            resp['status'] = 'failed'
            resp['msg']="Somehing went wrong!, please contact to system administrator..." + str(e)
            print(str(resp['msg']))
            return HttpResponse(json.dumps(resp), content_type="application/json")
        print('final')
        return HttpResponseRedirect("/department")

    else:
        return HttpResponse("<h1>404 - Page not found...")

@login_required(login_url='/accounts/login')
def delete_project(request):
    try:
        id = request.GET['id']
        Role_Master.objects.filter(Role_Id = id).delete()
        messages.warning(request, "Role id: "+str(id)+" Deleted successfully")
    except Exception as e:
        messages.error(request,"Somehing went wrong!, please contact to system administrator...")
    return HttpResponseRedirect("/role")

# End Project Views

# Profile Views 
def profile(request):
    emp = Emp_Master.objects.filter(Emp_Id = request.session.get('user_Emp_Id')).first()
    Dept_Active_List = Dept_Master.objects.filter(Dept_Status=True).all()
    Desg_Active_List = Designation_Master.objects.filter(Desg_Status=True,Dept_Id = emp.Dept_Id)
    Role_Active_List = Role_Master.objects.filter(Role_Status=True).all()
    Project_Active_List = Project_Master.objects.filter(Proj_Status=True).all()
    card_header='Details of Employee: '+emp.first_name + " " +emp.Middle_Name + " " +emp.last_name + "(Emp Id: " + str(emp.Emp_Id) + ")"
    context = {
        'employee' : emp,
        'card_header': card_header,
        'departments' : Dept_Active_List,
        'designations' : Desg_Active_List,
        'roles': Role_Active_List,
        'projects':Project_Active_List
    }
    return render(request, 'Employee/manage_emp.html',context)

# End Profile Views

# Employee Views
@login_required(login_url='/accounts/login')
def employee(request):
    emp_list = Emp_Master.objects.all()
    context = {
        'page_title':'Employee',
        'employees':emp_list,
    }
    return render(request, 'Employee/Employees.html',context)

@login_required(login_url='/accounts/login')
def manage_emp(request):
    
    card_header=''
    employee = {}
    data =  request.GET
    Dept_Active_List = Dept_Master.objects.filter(Dept_Status=True).all()
    Desg_Active_List = {}
    Role_Active_List = Role_Master.objects.filter(Role_Status=True).all()
    Project_Active_List = Project_Master.objects.filter(Proj_Status=True).all()
    id = ''
    details=''
    for key, value in data.items():
            print('Key: %s' % (key) ) 
            print('Value %s' % (value) )
    if 'id' in data:
        id = data['id']
    
    if 'details' in data:
        details = data['details']

    if id == '' and details == '':
        card_header='Create New Employee'
    else:
        if id != '':
            employee = Emp_Master.objects.filter(Emp_Id=id).first()
            Desg_Active_List = Designation_Master.objects.filter(Desg_Status=True,Dept_Id = employee.Dept_Id)
            print(employee.Dept_Id)
            card_header='Edit Employee: ' +employee.first_name + " " +employee.Middle_Name + " " +employee.last_name + "(Emp Id: " + str(employee.Emp_Id) + ")"

        if details != '':
            employee = Emp_Master.objects.filter(Emp_Id=details).first()
            Desg_Active_List = Designation_Master.objects.filter(Desg_Status=True,Dept_Id = employee.Dept_Id)
            print(employee.Role_Id)
            card_header='Details of Employee: '+employee.first_name + " " +employee.Middle_Name + " " +employee.last_name + "(Emp Id: " + str(employee.Emp_Id) + ")"
 

    print('Desg_Active_List: ' +str(Desg_Active_List))
    context = {
        'employee' : employee,
        'card_header': card_header,
        'departments' : Dept_Active_List,
        'designations' : Desg_Active_List,
        'roles': Role_Active_List,
        'projects':Project_Active_List,
        'details' : details
    }
    return render(request, 'Employee/manage_emp.html',context)

@login_required(login_url='/accounts/login')
def Get_Designation_EMP(request):
    if request.method == 'GET':
        data =  request.GET
        Dept_Id=''
        resp = {'status':'failed', 'designations': ''}
    else:
        return HttpResponse("<h1>404 - Page not found...")
    print("------------------All Key value Pairs-------------")
    for key, value in data.items():
        print('Key: %s' % (key) ) 
        print('Value %s' % (value) )
    print("------------------End All Key value Pairs-------------")
    try:
        if 'Dept_Id' in data:
            Dept_Id = data['Dept_Id']
        desg= list(Designation_Master.objects.filter(Desg_Status=True , Dept_Id = Dept_Id).values("Desg_Id","Desg_Name"))
        resp['status'] = 'success'
        print(desg)
        resp['designations'] =desg
        # serializers.serialize('json', qs)
        return HttpResponse(json.dumps(resp), content_type="application/json")
    except Exception as e:
        
        return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required(login_url='/accounts/login')
def save_emp(request):
    if request.method == 'POST':
        data =  request.POST
        
        print("------------------All Key value Pairs-------------")
        for key, value in data.items():
            print('Key: %s' % (key) ) 
            print('Value %s' % (value) )
        print("------------------End All Key value Pairs-------------")
        
        resp = {'status':'failed', 'msg': ''}
        is_active=''
        # Drop Down Validations
        if 'Proj_id' not in data:
            resp['status'] = 'failed'
            resp['msg']= "Please select Project from dropdown"
            return HttpResponse(json.dumps(resp), content_type="application/json")
    
        if 'Dept_Id' not in data:
            resp['status'] = 'failed'
            resp['msg']= "Please select Depratment from dropdown"
            return HttpResponse(json.dumps(resp), content_type="application/json")

        if 'Desg_Id' not in data:
            resp['status'] = 'failed'
            resp['msg']= "Please select Designation from dropdown"
            return HttpResponse(json.dumps(resp), content_type="application/json")                    

        if 'Role_Id' not in data:
            resp['status'] = 'failed'
            resp['msg']= "Please select Role from dropdown"
            return HttpResponse(json.dumps(resp), content_type="application/json")

        if 'Emp_Sex' not in data:
            resp['status'] = 'failed'
            resp['msg']= "Please select Gender"
            return HttpResponse(json.dumps(resp), content_type="application/json")   

        if 'is_active' in data:
            is_active = data['is_active']
            if is_active == 'on':
                is_active=True
        else:
            is_active=False              

        # Drop Down End of Validations

        # Get and set variables
        email = data['Email_ID']
        first_name=data['first_name']
        Middle_Name=data['Middle_Name']
        last_name=data['last_name']
        Contact_Number=re.sub('[^0-9]+', '', data['Contact_Number'])
        print(Contact_Number)
        date_joined=data['Joining_Date']
        Birth_Date=data['Birth_Date']
        Proj_id = data['Proj_id']
        Dept_Id= data['Dept_Id']
        Desg_Id=data['Desg_Id']
        Role_Id=data['Role_Id']
        Emp_Sex=data['Emp_Sex']
        
        # if Emp_Sex==1:
        #     Emp_Sex == "Male"
        # elif Emp_Sex==2:
        #     Emp_Sex == "Female"
        # else:
        #     Emp_Sex="Other"
        
        # End Get and set variables

        #Null values validation

        if email is None:
            resp['status'] = 'failed'
            resp['msg']= "Email Id is mandatory, please add Name"
            return HttpResponse(json.dumps(resp), content_type="application/json")
                
        if first_name is None:
            resp['status'] = 'failed'
            resp['msg']= "First Name is mandatory, please add Name"
            return HttpResponse(json.dumps(resp), content_type="application/json")
                
        if last_name is None:
            resp['status'] = 'failed'
            resp['msg']= "Last Name is mandatory, please add Name"
            return HttpResponse(json.dumps(resp), content_type="application/json")

        if Contact_Number is None:
            resp['status'] = 'failed'
            resp['msg']= "Contact Number is mandatory, please add Name"
            return HttpResponse(json.dumps(resp), content_type="application/json")

        if date_joined is None:
            resp['status'] = 'failed'
            resp['msg']= "Please select Joining Date"
            return HttpResponse(json.dumps(resp), content_type="application/json")

        if Birth_Date is None:
            resp['status'] = 'failed'
            resp['msg']= "Please select Birth Date"
            return HttpResponse(json.dumps(resp), content_type="application/json")

        # End Null Values Validation

        try:
            Proj = Project_Master.objects.filter(Proj_id=Proj_id).first()
            Desg = Designation_Master.objects.filter(Desg_Id = Desg_Id).first()
            Dept = Dept_Master.objects.filter(Dept_Id =Dept_Id).first()
            Role= Role_Master.objects.filter(Role_Id=Role_Id).first()

            print(Role.Role_Name)
            isExist = Emp_Master.isExists(email)
            print(isExist)
            print('Desg ' + str(Desg))
            Emp_Id  = ''
            if 'Emp_Id' in data:
                Emp_Id = data['Emp_Id']
            print('id:'+Emp_Id)
            # print('test: ' not isExist)
            if Emp_Id == '':
                
                if isExist == True:
                    resp['status'] = 'failed'
                    resp['msg']="Email id '"+email+"' is already exist, please use other Email id"
                    print(str(resp['msg']))
                    return HttpResponse(json.dumps(resp), content_type="application/json")
                # create_user
                pswd = Emp_Master.objects.make_random_password(length=14)

                save_Emp = Emp_Master(
                        email=email, 
                        password = pswd,
                        first_name = first_name,
                        Middle_Name = Middle_Name,
                        last_name=last_name,
                        Contact_Number=Contact_Number,
                        date_joined=date_joined,
                        Project_Id = Proj,
                        Dept_Id=Dept,
                        Desg_Id=Desg,
                        Role_Id=Role,
                        Emp_Sex=Emp_Sex,
                        Birth_Date=Birth_Date,
                        is_active= True
                    )
                save_Emp.save()

                subject = "Id creation in Roster Mangement"  
                msg     = f"""
                            Dear {first_name} {Middle_Name} {last_name},</br>
                            Your id has been created in Roster Mangement, please use below password to login. </br> 
                            Password: {pswd}."""
                from_id = "info@lbmrecruitment.com.au"
                res     = send_mail(subject, msg, from_id, email)  
                if(res == 1):  
                    msg = "Mail Sent Successfuly"  
                else:  
                    msg = "Mail could not sent"  


                messages.success(request, "Employee added successfully")   
                resp['status'] = 'success'
                return HttpResponse(json.dumps(resp), content_type="application/json")   
                # return HttpResponseRedirect('/department')  
                    
            else:
                Emp_Master.objects.filter(Emp_Id = Emp_Id).update(
                    email=email, 
                    first_name = first_name,
                    Middle_Name = Middle_Name,
                    last_name=last_name,
                    Contact_Number=Contact_Number,
                    date_joined=date_joined,
                    Project_Id = Proj,
                    Dept_Id=Dept,
                    Desg_Id=Desg,
                    Role_Id=Role,
                    Emp_Sex=Emp_Sex,
                    Birth_Date=Birth_Date,
                    is_active=is_active,
                    Modified_Date= datetime.datetime.now() 
                    )
                resp['status'] = 'success'
                messages.success(request, "Employee id: "+str(Emp_Id)+" updated successfully")  
                print(str(resp['msg']))
                return HttpResponse(json.dumps(resp), content_type="application/json")   
            
        except Exception as e:
            resp['status'] = 'failed'
            resp['msg']="Somehing went wrong!, please contact to system administrator..." + str(type(e))
            print(e)
            print(str(resp['msg']))
            return HttpResponse(json.dumps(resp), content_type="application/json")
        print('final')
        return HttpResponseRedirect("/department")
        
    else:
        return HttpResponse("<h1>404 - Page not found...")

@login_required(login_url='/accounts/login')
def delete_emp(request):
    try:
        id = request.GET['id']
        Emp_Master.objects.filter(Emp_Id = id).delete()
        messages.warning(request, "Employee id: "+str(id)+" Deleted successfully")
    except Exception as e:
        messages.error(request,"Somehing went wrong!, please contact to system administrator...")
    return HttpResponseRedirect("/employee")

# End Employee Views

# Shift Views
@login_required(login_url='/accounts/login')
def shift(request):
    shift_list = Shift_Master.objects.all()
    context = {
        'page_title':'Shifts',
        'shifts':shift_list,
    }
    return render(request, 'Employee/Shift/Shifts.html',context)

@login_required(login_url='/accounts/login')
def manage_shift(request):
    card_header=''
    shift = {}
    data =  request.GET
    id = ''
    details=''
    if 'id' in data:
        id = data['id']
        if id != '':
            shift = Shift_Master.objects.filter(Shift_Id=id).first()
        card_header='Edit the Shift'

    if 'details' in data:
        details = data['details']
        if details != '':
            shift = Shift_Master.objects.filter(Shift_Id=details).first()
            card_header='Details of Shift: ' + shift.Shift_Name
    
    if 'id' not in data and 'details' not in data:
        card_header='Create New Shift'

    context = {
        'shift' : shift,
        'card_header': card_header,
        'details' : details
    }
    return render(request, 'Employee/Shift/manage_shift.html',context)

@login_required(login_url='/accounts/login')
def delete_shift(request):
    try:
        id = request.GET['id']
        Shift_Master.objects.filter(Shift_Id = id).delete()
        messages.warning(request, "Shift id: "+str(id)+" Deleted successfully")
    except Exception as e:
        messages.error(request,"Somehing went wrong!, please contact to system administrator...")
    return HttpResponseRedirect("/shift")

@login_required(login_url='/accounts/login')
def save_shift(request):
    if request.method == 'POST':
        data =  request.POST
        Status=''
        resp = {'status':'failed', 'msg': ''}
        print("------------------All Key value Pairs-------------")
        for key, value in data.items():
            print('Key: %s' % (key) ) 
            print('Value %s' % (value) )
        print("------------------End All Key value Pairs-------------")
        Name = data['Shift_Name']
        Shift_Start_Time = data['Shift_Start_Time']
        Shift_End_Time = data['Shift_End_Time']

        isExist = Shift_Master.isExists(Name)
        print(isExist)

        try:
            ret = HttpResponse(json.dumps(resp), content_type="application/json")
            id  = ''
            if 'Shift_Id' in data:
                id = data['Shift_Id']
            print('id:'+id)
            # print('test: ' not isExist)
            if id == '':
                if Name is None:
                    resp['status'] = 'failed'
                    resp['msg']= "Name is mandatory, please add Name"
                    print(str(resp['msg']))
                    return HttpResponse(json.dumps(resp), content_type="application/json")
                
                if isExist == True:
                    resp['status'] = 'failed'
                    resp['msg']="Shift '"+Name+"' is already exist, please use other name"
                    print(str(resp['msg']))
                    # messages.error(request, "Department '"+Name+"' is already exist, please use other name")
                    return HttpResponse(json.dumps(resp), content_type="application/json")
                
                save_shift = Shift_Master(
                    Shift_Name=Name, 
                    Shift_Start_Time = Shift_Start_Time,
                    Shift_End_Time = Shift_End_Time)
                save_shift.save()
                messages.success(request, "Shift added successfully")   
                resp['status'] = 'success'
                    
            else:
                print("Now: "+str(datetime.datetime.now()))
                Shift_Master.objects.filter(Shift_Id = id).update(
                    Shift_Name = Name,
                    Shift_Start_Time=Shift_Start_Time,
                    Shift_End_Time = Shift_End_Time, 
                    Modified_Date = datetime.datetime.now()  )
                resp['status'] = 'success'
                messages.success(request, "Shift id: "+str(id)+" updated successfully")  
                print(str(resp['msg']))
        except Exception as e:
            resp['status'] = 'failed'
            resp['msg']="Somehing went wrong!, please contact to system administrator..." + str(type(e))
            print(str(resp['msg']))
            print(e)
        print('final')
        return HttpResponseRedirect("/department")

    else:
        return HttpResponse("<h1>404 - Page not found...")

# End Shift Views

# Assign Shift Views
@login_required(login_url='/accounts/login')
def assign_shift(request):
    assign_shift_list = Employee_Shift_Master.objects.all()
    context = {
        'page_title':'Employee',
        'assign_shifts':assign_shift_list,
    }
    return render(request, 'Employee/Shift/Assign_Shift.html',context)

@login_required(login_url='/accounts/login')
def manage_assign_shift(request):
    card_header=''
    assign_shift = {}
    data =  request.GET
    Emp_Active_List = Emp_Master.objects.filter(is_active=True).all()
    Shift_Active_List = Shift_Master.objects.all()
    id = ''
    details=''
    if 'id' in data:
        id = data['id']
        if id != '':
            assign_shift = Employee_Shift_Master.objects.filter(Emp_Shift_Id=id).first()
        card_header='Edit the employee assigned shift'

    if 'details' in data:
        details = data['details']
        if details != '':
            assign_shift = Employee_Shift_Master.objects.filter(Emp_Shift_Id=details).first()
            card_header='Details of assigned shift: ' + details 

    if 'id' not in data and 'details' not in data:
        card_header='Assign Shift'
    #print(assign_shift.Shift_End_Time)
    context = {
        'assign_shift' : assign_shift,
        'employees' : Emp_Active_List,
        'shifts': Shift_Active_List,
        'card_header': card_header,
        'details' : details
    }
    return render(request, 'Employee/Shift/manage_assign_shift.html',context)

@login_required(login_url='/accounts/login')
def Get_Assign_Shifts_Time(request):
    resp = {'status':'failed','Shift_Start_Time': '','Shift_End_Time': ''}
    Shift_Id=''
    shift_details=''
    if request.method == 'GET':
        data =  request.GET
    else:
        return HttpResponse("<h1>404 - Page not found...")
    print("------------------All Key value Pairs-------------")
    for key, value in data.items():
        print('Key: %s' % (key) ) 
        print('Value %s' % (value) )
    print("------------------End All Key value Pairs-------------")
        
    try:
        print('STrat-------')
        if 'Shift_Id' in data:
            Shift_Id = data['Shift_Id']
        shift_details = Shift_Master.objects.filter(Shift_Id = Shift_Id).values("Shift_Start_Time","Shift_End_Time").first()
        print('str details:: ' + str(shift_details))
        # for shift in shift_details:
        # print(shift)
        resp['Shift_Start_Time'] = shift_details['Shift_Start_Time'].strftime("%H:%M")
        resp['Shift_End_Time'] = shift_details['Shift_End_Time'].strftime("%H:%M")
        resp['status'] = 'success'
        print(resp['Shift_Start_Time'])
        print(resp['status'])
        return HttpResponse(json.dumps(resp), content_type="application/json")
    except Exception as e:
        print(e)
        return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required(login_url='/accounts/login')
def delete_assign_shift(request):
    try:
        id = request.GET['id']
        Employee_Shift_Master.objects.filter(Emp_Shift_Id=id).delete()
        messages.warning(request, "Shift has been Deleted successfully")
    except Exception as e:
        messages.error(request,"Somehing went wrong!, please contact to system administrator...")
    return HttpResponseRedirect("/assign_shift")

@login_required(login_url='/accounts/login')
def save_assign_shift(request):
    if request.method == 'POST':
        data =  request.POST
        
        print("------------------All Key value Pairs-------------")
        for key, value in data.items():
            print('Key: %s' % (key) ) 
            print('Value %s' % (value) )
        print("------------------End All Key value Pairs-------------")
        
        resp = {'status':'failed', 'msg': ''}

        # Drop Down Validations
        if 'Emp_Id' not in data:
            resp['status'] = 'failed'
            resp['msg']= "Please select Employee from dropdown"
            return HttpResponse(json.dumps(resp), content_type="application/json")

        if 'Shift_Id' not in data:
            resp['status'] = 'failed'
            resp['msg']= "Please select Shift from dropdown"
            return HttpResponse(json.dumps(resp), content_type="application/json")                          

        # Drop Down End of Validations

        # Get and set variables
        Emp_Id= data['Emp_Id']
        Shift_Id=data['Shift_Id']
        Start_Date=data['Start_Date']
        End_Date=data['End_Date']
        Emp_Shift_Id=''
        print('Shift_Id '+ str(type(Shift_Id)))
        print(data['Shift_Start_Time'])
        try:
            if 'Emp_Shift_Id' in data:
                Emp_Shift_Id=data['Emp_Shift_Id'] 
            
            Emp = Emp_Master.objects.filter(Emp_Id = Emp_Id).first()
            Shift = Shift_Master.objects.filter(Shift_Id =Shift_Id).first()

            if(Shift_Id == '1'):
                Shift_Start_Time=data['Shift_Start_Time']
                Shift_End_Time=data['Shift_End_Time'] 
            else:
                Shift_Start_Time = Shift.Shift_Start_Time
                Shift_End_Time = Shift.Shift_End_Time
            
            if Emp_Shift_Id == '':
                shift_details_start_date = Employee_Shift_Master.objects.filter(
                    Emp_Id=Emp,
                    Start_Date__lte=Start_Date,
                    End_Date__gte=Start_Date
                    ).first()

                shift_details_end_date = Employee_Shift_Master.objects.filter(
                    Emp_Id=Emp,
                    Start_Date__lte=End_Date,
                    End_Date__gte=End_Date
                    ).first()

            else:
                shift_details_start_date = Employee_Shift_Master.objects.exclude(Emp_Shift_Id = Emp_Shift_Id).filter(
                    Emp_Id=Emp,
                    Start_Date__lte=Start_Date,
                    End_Date__gte=Start_Date
                    ).first()

                shift_details_end_date = Employee_Shift_Master.objects.exclude(Emp_Shift_Id = Emp_Shift_Id).filter(
                    Emp_Id=Emp,
                    Start_Date__lte=End_Date,
                    End_Date__gte=End_Date
                    ).first()

            if(shift_details_start_date != None):
                resp['msg']="Start Date is already mapped to selected user"
                return HttpResponse(json.dumps(resp), content_type="application/json")  

            if(shift_details_end_date != None):
                resp['msg']="End Date is already mapped to selected user"
                return HttpResponse(json.dumps(resp), content_type="application/json") 

            print(Shift_Start_Time)
            Emp_Shift_Id  = ''
            if 'Emp_Shift_Id' in data:
                Emp_Shift_Id = data['Emp_Shift_Id']
            print('id:'+Emp_Shift_Id)
            # print('test: ' not isExist)
            if Emp_Shift_Id == '':
                save_Emp_Shift = Employee_Shift_Master(
                        Emp_Id=Emp,
                        Shift_Id=Shift,
                        Start_Date=Start_Date,
                        End_Date=End_Date,
                        Shift_Start_Time=Shift_Start_Time,
                        Shift_End_Time=Shift_End_Time
                    )
                save_Emp_Shift.save()
                messages.success(request, "Record added successfully")   
                resp['status'] = 'success'
                    
            else:
                Employee_Shift_Master.objects.filter(Emp_Shift_Id = Emp_Shift_Id).update(
                    Emp_Id=Emp,
                    Shift_Id=Shift,
                    Start_Date=Start_Date,
                    End_Date=End_Date,
                    Shift_Start_Time=Shift_Start_Time,
                    Shift_End_Time=Shift_End_Time
                    )
                resp['status'] = 'success'
                messages.success(request, "Record updated successfully")  
                print(str(resp['msg'])) 
            
        except Exception as e:
            resp['status'] = 'failed'
            resp['msg']="Somehing went wrong!, please contact to system administrator..." + str(e)
            print(e)
            print(str(resp['msg']))
        print('final')
        return HttpResponse(json.dumps(resp), content_type="application/json")  
        
    else:
        return HttpResponse("<h1>404 - Page not found...")

# End Assign Shift Views
@login_required(login_url='/accounts/login')
def shift_calender(request):
    assign_shift_list = Employee_Shift_Master.objects.all()
    emp_active_list = Emp_Master.objects.all()
    shift_list=Shift_Master.objects.all()
    context = {
        'page_title':'Employee',
        'employees' : emp_active_list,
        'shifts' : shift_list,
        'assign_shifts':assign_shift_list,
    }
    return render(request, 'Employee/Shift/Shift_Calender.html',context)

@login_required(login_url='/accounts/login')
def Get_Assigned_Shifts(request):
    if request.method == 'GET':
        data =  request.GET
        
        print("------------------All Key value Pairs-------------")
        for key, value in data.items():
            print('Key: %s' % (key) ) 
            print('Value %s' % (value) )
        print("------------------End All Key value Pairs-------------")

        assign = Employee_Shift_Master.objects.filter(Emp_Id=data['Emp_Id'])
        Shif_Names= assign.distinct()
        print(Shif_Names)
        shifts=[]
        for t in assign:
            if not shifts.__contains__(t.Shift_Id.Shift_Name):
                shifts.append(str(t.Shift_Id.Shift_Name) + ' (' + str(t.Shift_Start_Time.strftime("%I:%M %p")) + ' - ' + str(t.Shift_End_Time.strftime("%I:%M %p"))+')')
        print(shifts)
        resp = {'status':'failed', 'shift_data': '' , 'shifts' : ''}
        Final_Json_Data=[]
        print("start -------------------------")
        for item in assign:
            r = lambda: random.randint(0,255)
            Final_Json_Data.append(
                {
                    'title': str(item.Shift_Id.Shift_Name) + ' (' + str(item.Shift_Start_Time.strftime("%I:%M %p")) + ' - ' + str(item.Shift_End_Time.strftime("%I:%M %p"))+')',
                    'Start_Date': + (item.Start_Date-datetime.date.today()).days,
                    'length':abs((item.Start_Date-item.End_Date).days),
                }
                )
            print((item.Start_Date-datetime.date.today()).days)
        # print(test)
        resp['status'] = 'success'
        resp['shift_data'] = Final_Json_Data
        resp['shifts'] = shifts
        
    return HttpResponse(json.dumps(resp), content_type="application/json")
# Shift Calender

# End Shift Calender

# Attendance
@login_required(login_url='/accounts/login')
def timesheet(request):
    timesheet_list = Attendance_Master.objects.all()
    context = {
        'page_title':'Timesheet',
        'timesheets':timesheet_list,
    }
    for t in timesheet_list:
        print(str(t.Attendance_Date))
    return render(request, 'Employee/Attendance/Timesheets.html',context)

@login_required(login_url='/accounts/login')
def mark_attendance(request):
    Emp_Active_List = Emp_Master.objects.filter(is_active=True).all()
    timesheet_list_today = Attendance_Master.objects.filter(Attendance_Date=datetime.date.today())
    Shift_Details = Employee_Shift_Master.objects.filter()
    card_header='Mark the attendance' 

    context = {
        'employees' : Emp_Active_List,
        'card_header': card_header,
        'timesheets':timesheet_list_today,
        'todays_date': datetime.date.today()
    }
    return render(request, 'Employee/Attendance/Mark_Attendance.html',context)

@login_required(login_url='/accounts/login')
def Clock_In_Clock_Out_Old(request):
    if request.method == 'POST':
        data =  request.POST
        resp = {'status':'failed', 'msg': ''}
        print("------------------All Key value Pairs-------------")
        for key, value in data.items():
            print('Key: %s' % (key) ) 
            print('Value %s' % (value) )
        print("------------------End All Key value Pairs-------------")
        
        Emp_Id=''
        Emp=''
        Attendance_Id=''
        btn_clock_in_clock_out=''
        Att_Type_Code = ''
        current_Time = datetime.datetime.now().time()
        current_Date = datetime.date.today()
        sift_start_time = ''

        if 'Emp_Id' in data:
            Emp_Id = data['Emp_Id']
            Emp = Emp_Master.objects.filter(Emp_Id = Emp_Id).first()
        if 'Attendance_Id' in data:
            Attendance_Id = data['Attendance_Id']
        if 'btn_clock_in_clock_out' in data:
            btn_clock_in_clock_out = data['btn_clock_in_clock_out']

        try:
            shift_details_today = Employee_Shift_Master.objects.filter(
                Emp_Id=Emp_Id,
                Start_Date__lte=datetime.date.today(),
                End_Date__gte=datetime.date.today()
                ).first()
        
            # if shift_details_today == None:
            #     Att_Type_Code='P'
            # else:
            shift_start_time = shift_details_today.Shift_Start_Time
            
            shift_time_Minus_clockin_time = datetime.datetime.combine(datetime.date.today(), current_Time) - datetime.datetime.combine(datetime.date.today(), shift_start_time)
            
            delta_hours = shift_time_Minus_clockin_time.days * 24 + shift_time_Minus_clockin_time.seconds / 3600.0
            print('shift_time_Minus_clockin_time' + str(delta_hours))
            
            if delta_hours > 1:
                Att_Type_Code='PL'
            else:
                Att_Type_Code='P'
            print(Att_Type_Code)
            if btn_clock_in_clock_out == "Punch In":
                
                save_attendance = Attendance_Master(
                    Emp_Id=Emp,
                    Attendance_Date=current_Date,
                    Clock_In_Time = current_Time,
                    Attendance_Type_Id = Attendance_Type.objects.filter(Attendance_Type_Code = Att_Type_Code).first()
                    )
                save_attendance.save()
                resp['msg']=str("Attendance has been marked successfully for user: " + 
                shift_details_today.Emp_Id.first_name + " " + shift_details_today.Emp_Id.Middle_Name +  " " + shift_details_today.Emp_Id.last_name)
            
            elif btn_clock_in_clock_out == "Punch Out":
                print("test")
                current_time = datetime.datetime.now().time()
                print(current_time)
                clock_in=Attendance_Master.objects.filter(Attendance_Id = Attendance_Id).first()
                #print(clock_in.Emp_Id.)
                att_Type_Code = Attendance_Master.attendance_code(
                     datetime.datetime.combine(datetime.date.today(), current_time) - datetime.datetime.combine(datetime.date.today(), clock_in.Clock_In_Time)
                    )

                print(att_Type_Code.Attendance_Type_Name)

                resp['msg'] =str("Clocked out successfully for user: " +
                shift_details_today.Emp_Id.first_name + " " + shift_details_today.Emp_Id.Middle_Name +  " " + shift_details_today.Emp_Id.last_name)
            
            resp['status'] = 'success'
            print(str(resp['status'] ))
            print(str(resp['msg'] ))
            return HttpResponse(json.dumps(resp), content_type="application/json")

        except Exception as e:
            resp['msg'] =str("Something went wrong please contact to system admin." + str(e))
            return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required(login_url='/accounts/login')         
def Clock_In_Clock_Out(request):
    if request.method == 'POST':
        data =  request.POST
        resp = {'status':'failed', 'msg': ''}
        print("------------------All Key value Pairs-------------")
        for key, value in data.items():
            print('Key: %s' % (key) ) 
            print('Value %s' % (value) )
        print("------------------End All Key value Pairs-------------")
        
        resp = {'status':'failed', 'shift_data': ''}
        Emp_Id=''
        Attendance_Id=''
        btn_clock_in_clock_out=''
        Att_Type_Code = ''
        current_Time = datetime.datetime.now().time()
        current_Date = datetime.date.today()
        sift_start_time = ''

        if 'Emp_Id' in data:
            Emp_Id = data['Emp_Id']
        if 'Attendance_Id' in data:
            Attendance_Id = data['Attendance_Id']
        if 'Emp_Shift_Id' in data:
            Emp_Shift_Id = data['Emp_Shift_Id']
        try:
            Emp = Emp_Master.objects.filter(Emp_Id=Emp_Id).first()
            Att_Type = Attendance_Type.objects.filter(Attendance_Type_Code = "P").first()
            Emp_Shift = Employee_Shift_Master.objects.filter(Emp_Id=Emp_Id).first()
            
            print(Emp)
            if(Attendance_Id == ''):
                save_attendance = Attendance_Master(
                Emp_Id=Emp,
                Attendance_Date=current_Date,
                Clock_In_Time = current_Time,
                Attendance_Type_Id = Att_Type,
                Emp_Shift_Id=Emp_Shift
                )
                save_attendance.save()
                
                resp['msg']=str("Attendance has been marked successfully for user: " + 
                Emp.first_name + " " + Emp.Middle_Name +  " " + Emp.last_name)
            else:
                Attendance_Master.objects.filter(Attendance_Id = Attendance_Id).update(
                    Clock_Out_Time = current_Time,
                    # Attendance_Type_Id=att_Type_Code
                )
                print('Out')
                resp['msg']=str("Attendance has been marked successfully for user: " + 
                Emp.first_name + " " + Emp.Middle_Name +  " " + Emp.last_name)
            
            resp['status'] = 'success'
        except Exception as e:
            print(e)
            resp['msg'] =str("Something went wrong please contact to system admin." + str(e))
    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required(login_url='/accounts/login')
def Get_Shift_Details(request):
    resp = {'Shift_Start_Time': '','Shift_End_Time': '', 'attendance_Status': None, 'Attendance_Id':'','Emp_Shift_Id':''}
    if request.method == 'GET':
        data =  request.GET
    print("------------------All Key value Pairs-------------")
    for key, value in data.items():
        print('Key: %s' % (key) ) 
        print('Value %s' % (value) )
    print("------------------End All Key value Pairs-------------")
    # emp = Emp_Master.objects.filter(Emp_Id=data['Emp_Id']).first()
    Emp_Id= request.session.user_Emp_Id 
    if 'Emp_Id' in data:
        Emp_Id = data['Emp_Id']
    else:
        Emp_Id=[]

    is_Shift_Assigned = Employee_Shift_Master.objects.filter(
        Emp_Id=Emp_Id,
        Start_Date__lte=datetime.date.today(),
        End_Date__gte=datetime.date.today()
        ).first()
    if not is_Shift_Assigned :
        print("No data")
        resp['attendance_Status'] = "No Shift"
    else:
        resp['Shift_Start_Time']=str(is_Shift_Assigned.Shift_Start_Time.strftime("%I:%M %p"))
        resp['Shift_End_Time']=str(is_Shift_Assigned.Shift_End_Time.strftime("%I:%M %p"))  
        resp['Emp_Shift_Id'] = str(is_Shift_Assigned.Emp_Shift_Id)
        
        shift_time_Minus_current_time = datetime.datetime.combine(datetime.date.today(), datetime.datetime.now().time()) - datetime.datetime.combine(datetime.date.today(), is_Shift_Assigned.Shift_Start_Time)
        delta_mins = shift_time_Minus_current_time.days * 24 + shift_time_Minus_current_time.seconds / 60.0
        print(delta_mins)
        # if(is_Shift_Assigned.Shift_Id.Shift_Id == '1'):
        #     if(+delta_mins > 30):

        is_Att_Marked =Attendance_Master.is_attendance_marked(Emp_Id,datetime.date.today())
    
        print(is_Att_Marked)
        if is_Att_Marked == False:
            resp['attendance_Status']=is_Att_Marked
        else:
            resp['attendance_Status']=is_Att_Marked[0]
            resp['Attendance_Id'] = is_Att_Marked[1]

    print('attendanc marked:' + str(resp['attendance_Status']))
    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required(login_url='/accounts/login')
def attendance_calender(request):
    assign_shift_list = Employee_Shift_Master.objects.all()
    emp_active_list = Emp_Master.objects.all()
    shift_list=Shift_Master.objects.all()
    context = {
        'page_title':'Employee',
        'employees' : emp_active_list,
        'shifts' : shift_list,
        'assign_shifts':assign_shift_list,
    }
    return render(request, 'Employee/Attendance/Attendance_Calender.html',context)

@login_required(login_url='/accounts/login')
def Get_Calender_Details(request):
    resp = {'status':'failed', 'shift_data': ''}
    if request.method == 'GET':
        data =  request.GET
        print("------------------All Key value Pairs-------------")
        for key, value in data.items():
            print('Key: %s' % (key) ) 
            print('Value %s' % (value) )
        print("------------------End All Key value Pairs-------------")
        
        # Get the data from models
        EMP = Emp_Master.objects.filter(Emp_Id =data['Emp_Id']).first()
        attendance_mark_details = Attendance_Master.objects.filter(Emp_Id=EMP)
        #End Get the data from models

        print(EMP)
        emp_Joining_Date = EMP.date_joined
        print(emp_Joining_Date)
        print(attendance_mark_details)

        # variabl declartion
        i=0
        Final_Json_Data=[]
        Already_Added_Dates=[]
        bg_Color = '' 
        delta = datetime.datetime.now().date() - emp_Joining_Date.date()
        print(delta.days)
        print("start -------------------------")
  
        for att_data in attendance_mark_details:
            dt_diff = + (att_data.Attendance_Date-datetime.date.today()).days
            
            if  att_data.Attendance_Type_Id.Attendance_Type_Name == "Present":
                bg_Color = 'Green'
            elif att_data.Attendance_Type_Id.Attendance_Type_Name == "Present (Late)":
                bg_Color = 'chartreuse'
            else:
                bg_Color = 'yellow'

            print("in " + str(att_data.Clock_In_Time))
            print("out  " + str(att_data.Clock_Out_Time))

            in_time = att_data.Clock_In_Time
            # To handle no outtime punch
            if att_data.Clock_Out_Time is None:
                clock_out_hr = (datetime.datetime.combine(datetime.date(1,1,1),in_time) + datetime.timedelta(hours = 1)).strftime("%H")
                clock_out_min = '0'
                bg_Color = 'black'
                att_tye_id_msg = "No Out Time is Punched"
            else:
                clock_out_hr = att_data.Clock_Out_Time.strftime("%H")
                clock_out_min = att_data.Clock_Out_Time.strftime("%M")
                att_tye_id_msg = att_data.Attendance_Type_Id.Attendance_Type_Name
            print('clock_out_hr' + str(clock_out_hr))
            print(str(att_data.Clock_In_Time.strftime("%H")))
            
            # avaiable attendance data addition in Final_json -----------------
            Final_Json_Data.append(
            {
                # 'Attendance_Date' : data.Attendance_Date,
                'Attendance_Date_Diff': dt_diff,

                'Clock_In_Time_Hr': att_data.Clock_In_Time.strftime("%H"),
                'Clock_In_Time_Minute': att_data.Clock_In_Time.strftime("%M"),

                'Clock_Out_Time_Hr': clock_out_hr,
                'Clock_Out_Time_Minute': clock_out_min,

                'backgroundColor': bg_Color,
                'allDay': False,

                'Attendance_Type_Id' : att_tye_id_msg
            }
            )
            Already_Added_Dates.append(str(dt_diff))
            # End avaiable attendance data addition in Final_json -----------------
        print('Already_Added_Dates' + str(Already_Added_Dates))
        
        while i<(delta.days+1):
            dt = emp_Joining_Date + timedelta(days = i)
            # print("Yesterday was: ", dt)
            dt_diff = + (dt.date() - datetime.date.today()).days
            print(str(dt_diff)+ ' i: ' + str(i) + ' delta days: ' + str(delta.days+1) + ' dt: ' + str(dt))
            if(str(dt_diff) not in Already_Added_Dates):
                test = Employee_Shift_Master.objects.filter(
                    Emp_Id=data['Emp_Id'],
                    Start_Date__lte=dt,
                    End_Date__gte=dt
                    ).first()
                    #End Get the
                if test != None:
                    att_type_id = 'Absent'
                    bg_Color = 'Red'
                else:
                    att_type_id = 'No Shift Mapped'
                    bg_Color= 'orange'

                Final_Json_Data.append(
                    {
                    'Attendance_Date_Diff': dt_diff,
                    
                    'Clock_In_Time_Hr': "00",
                    'Clock_In_Time_Minute': "00",

                    'Clock_Out_Time_Hr': "00",
                    'Clock_Out_Time_Minute': "00",

                    'backgroundColor': bg_Color,
                    'allDay': True,

                    'Attendance_Type_Id' : att_type_id
                    }
                    )

            i=i+1
        
        print(Final_Json_Data)
        # print(Final_Json_Data)
        resp['status'] = 'success'
        resp['shift_data'] = Final_Json_Data
        return HttpResponse(json.dumps(resp), content_type="application/json")

# ENd Attendance