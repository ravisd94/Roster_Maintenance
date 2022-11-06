import datetime
from msilib.schema import _Validation
from urllib import response
from xml.dom import ValidationErr
from django.shortcuts import render
from .models import Emp_Master,Dept_Master,Designation_Master, Role_Master, Shift_Master, Employee_Shift_Master
from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
import json
from django.contrib import messages #import messages
from django import forms
from .forms import RoleForm_Add
import re

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

# Department Views
def department(request):
    department_list = Dept_Master.objects.all()
    context = {
        'page_title':'Departments',
        'departments':department_list,
    }
    return render(request, 'Employee/Department/Departments.html',context)

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

def delete_dept(request):
    try:
        id = request.GET['id']
        Dept_Master.objects.filter(Dept_Id = id).delete()
        messages.warning(request, "Department id: "+str(id)+" Deleted successfully")
    except Exception as e:
        messages.error(request,"Somehing went wrong!, please contact to system administrator...")
    return HttpResponseRedirect("/department")

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
def designation(request):
    designation_list = Designation_Master.objects.all()
    context = {
        'page_title':'Designation',
        'designations':designation_list,
    }
    return render(request, 'Employee/Designation/Designations.html',context)

def manage_desg(request):
    card_header=''
    designation = {}
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

    context = {
        'designation' : designation,
        'card_header': card_header,
        'details' : details
    }
    return render(request, 'Employee/Designation/manage_designation.html',context)

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
            if 'Desg_Id' in data:
                id = data['Desg_Id']
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
                
                save_designation = Designation_Master(Desg_Name=Name, Desg_description = Desc,Desg_Status = True)
                save_designation.save()
                messages.success(request, "Designation added successfully")   
                resp['status'] = 'success'
                return HttpResponse(json.dumps(resp), content_type="application/json")   
                # return HttpResponseRedirect('/department')  
                    
            else:
                print("Now: "+str(datetime.datetime.now()))
                Designation_Master.objects.filter(Desg_Id = id).update(
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
            resp['msg']="Somehing went wrong!, please contact to system administrator..." + str(type(e))
            print(str(resp['msg']))
            return HttpResponse(json.dumps(resp), content_type="application/json")
        print('final')
        return HttpResponseRedirect("/designation")
        # return department()
        # return render(request,'Employee/Department/Departments.html',{'msg':msg})
    # return HttpResponse(json.dumps(resp), content_type="application/json")
    else:
        return HttpResponse("<h1>404 - Page not found...")















    if request.method == 'POST':
        data =  request.POST
        Status=''
        for key, value in data.items():
            print('Key: %s' % (key) ) 
            print('Value %s' % (value) )

        Name = data['Desg_Name']
        Desc = data['Desg_description']

        isExist = Designation_Master.isExists(Name)
        print(isExist)

        if 'Desg_Status' in data:
            Status = data['Desg_Status']
            if Status == 'on':
                Status=True
        else:
            Status=False
        print("status: "+str(Status))
        try:
            id  = ''
            if 'Desg_Id' in data:
                id = data['Desg_Id']
            print('id:'+id)
            # print('test: ' not isExist)
            if id == '':
                if Name is None:
                   return HttpResponse("Name is mendatory, please add Name.",content_type='text/plain') 
                if isExist == False:
                    save_department = Designation_Master(Desg_Name=Name, Desg_description = Desc,Desg_Status = Status)
                    save_department.save()
                    messages.success(request, "Designation added successfully")
                else:
                    messages.error(request,"Designation "+Name+" is already exist, please use other name")
                    return HttpResponse("Name is already exist, please use other name",content_type='text/plain')
                    # return HttpResponseRedirect("/designation/manage")
                    # return render(request, 'Employee/Department/manage_department.html')
                    
            else:
                Designation_Master.objects.filter(Desg_Id = id).update(Desg_Name = Name,Desg_Status=Status,Desg_description = Desc)
                messages.success(request, "Designation id: "+str(id)+" updated successfully")
            
        except Exception as e:
            messages.error(request,"Somehing went wrong!, please contact to system administrator..." + str(type(e)))

        return HttpResponseRedirect("/designation")
    else:
        return HttpResponse("<h1>404 - Page not found...")

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
def role(request):
    role_list = Role_Master.objects.all()
    context = {
        'page_title':'Role',
        'roles':role_list,
    }
    return render(request, 'Employee/Role/Roles.html',context)

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

def project(request):
    role_list = Role_Master.objects.all()
    context = {
        'page_title':'Role',
        'roles':role_list,
    }
    return render(request, 'Employee/Role/Roles.html',context)

def manage_project(request):
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

def delete_project(request):
    try:
        id = request.GET['id']
        Role_Master.objects.filter(Role_Id = id).delete()
        messages.warning(request, "Role id: "+str(id)+" Deleted successfully")
    except Exception as e:
        messages.error(request,"Somehing went wrong!, please contact to system administrator...")
    return HttpResponseRedirect("/role")

# End Project Views
def employee(request):
    emp_list = Emp_Master.objects.all()
    context = {
        'page_title':'Employee',
        'employees':emp_list,
    }
    return render(request, 'Employee/Employees.html',context)

def manage_emp(request):
    card_header=''
    employee = {}
    data =  request.GET
    Dept_Active_List = Dept_Master.objects.filter(Dept_Status=True).all()
    Desg_Active_List = Designation_Master.objects.filter(Desg_Status=True).all()
    Role_Active_List = Role_Master.objects.filter(Role_Status=True).all()
    id = ''
    details=''
    for key, value in data.items():
            print('Key: %s' % (key) ) 
            print('Value %s' % (value) )
    if 'id' in data:
        id = data['id']
        if id == '':
            card_header='Create New '
        else:
            employee = Emp_Master.objects.filter(Emp_Id=id).first()
            print(employee.First_Name)
        card_header='Edit '

    if 'details' in data:
        details = data['details']
        if details != '':
            employee = Emp_Master.objects.filter(Emp_Id=details).first()
            print(employee.Role_Id)
            card_header='Details of Employee'
 
    print('details: ' + details)
    context = {
        'employee' : employee,
        'card_header': card_header,
        'departments' : Dept_Active_List,
        'designations' : Desg_Active_List,
        'roles': Role_Active_List,
        'details' : details
    }
    return render(request, 'Employee/manage_emp.html',context)

def save_emp(request):
    if request.method == 'POST':
        data =  request.POST
        
        print("------------------All Key value Pairs-------------")
        for key, value in data.items():
            print('Key: %s' % (key) ) 
            print('Value %s' % (value) )
        print("------------------End All Key value Pairs-------------")
        
        resp = {'status':'failed', 'msg': ''}
        Emp_Status=''
        # Drop Down Validations
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

        if 'Emp_Status' in data:
            Emp_Status = data['Emp_Status']
            if Emp_Status == 'on':
                Emp_Status=True
        else:
            Emp_Status=False              

        # Drop Down End of Validations

        # Get and set variables
        Email_ID = data['Email_ID']
        First_Name=data['First_Name']
        Middle_Name=data['Middle_Name']
        Last_Name=data['Last_Name']
        Contact_Number=re.sub('[^0-9]+', '', data['Contact_Number'])
        print(Contact_Number)
        Joining_Date=data['Joining_Date']
        Birth_Date=data['Birth_Date']

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

        if Email_ID is None:
            resp['status'] = 'failed'
            resp['msg']= "Email Id is mandatory, please add Name"
            return HttpResponse(json.dumps(resp), content_type="application/json")
                
        if First_Name is None:
            resp['status'] = 'failed'
            resp['msg']= "First Name is mandatory, please add Name"
            return HttpResponse(json.dumps(resp), content_type="application/json")
                
        if Last_Name is None:
            resp['status'] = 'failed'
            resp['msg']= "Last Name is mandatory, please add Name"
            return HttpResponse(json.dumps(resp), content_type="application/json")

        if Contact_Number is None:
            resp['status'] = 'failed'
            resp['msg']= "Contact Number is mandatory, please add Name"
            return HttpResponse(json.dumps(resp), content_type="application/json")

        if Joining_Date is None:
            resp['status'] = 'failed'
            resp['msg']= "Please select Joining Date"
            return HttpResponse(json.dumps(resp), content_type="application/json")

        if Birth_Date is None:
            resp['status'] = 'failed'
            resp['msg']= "Please select Birth Date"
            return HttpResponse(json.dumps(resp), content_type="application/json")

        # End Null Values Validation

        try:
            Desg = Designation_Master.objects.filter(Desg_Id = Desg_Id).first()
        
            Dept = Dept_Master.objects.filter(Dept_Id =Dept_Id).first()

            Role= Role_Master.objects.filter(Role_Id=Role_Id).first()
            print(Role.Role_Name)
            isExist = Emp_Master.isExists(Email_ID)
            print(isExist)

            Emp_Id  = ''
            if 'Emp_Id' in data:
                Emp_Id = data['Emp_Id']
            print('id:'+Emp_Id)
            # print('test: ' not isExist)
            if Emp_Id == '':
                
                if isExist == True:
                    resp['status'] = 'failed'
                    resp['msg']="Email id '"+Email_ID+"' is already exist, please use other Email id"
                    print(str(resp['msg']))
                    return HttpResponse(json.dumps(resp), content_type="application/json")
                
                save_Emp = Emp_Master(
                        Email_ID=Email_ID, 
                        First_Name = First_Name,
                        Middle_Name = Middle_Name,
                        Last_Name=Last_Name,
                        Dept_Id=Dept,
                        Contact_Number=Contact_Number,
                        Joining_Date=Joining_Date,
                        Desg_Id=Desg,
                        Role_Id=Role,
                        Emp_Sex=Emp_Sex,
                        Birth_Date=Birth_Date,
                        Emp_Status=True
                    )
                save_Emp.save()
                messages.success(request, "Employee added successfully")   
                resp['status'] = 'success'
                return HttpResponse(json.dumps(resp), content_type="application/json")   
                # return HttpResponseRedirect('/department')  
                    
            else:
                Emp_Master.objects.filter(Emp_Id = Emp_Id).update(
                    Email_ID=Email_ID, 
                    First_Name = First_Name,
                    Middle_Name = Middle_Name,
                    Last_Name=Last_Name,
                    Dept_Id=Dept,
                    Contact_Number=Contact_Number,
                    Joining_Date=Joining_Date,
                    Desg_Id=Desg,
                    Role_Id=Role,
                    Emp_Sex=Emp_Sex,
                    Birth_Date=Birth_Date,
                    Emp_Status=Emp_Status,
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
def shift(request):
    shift_list = Shift_Master.objects.all()
    context = {
        'page_title':'Shifts',
        'shifts':shift_list,
    }
    return render(request, 'Employee/Shift/Shifts.html',context)

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

def delete_shift(request):
    try:
        id = request.GET['id']
        Shift_Master.objects.filter(Dept_Id = id).delete()
        messages.warning(request, "Shift id: "+str(id)+" Deleted successfully")
    except Exception as e:
        messages.error(request,"Somehing went wrong!, please contact to system administrator...")
    return HttpResponseRedirect("/shift")

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

        # if 'Dept_Status' in data:
        #     Status = data['Dept_Status']
        #     if Status == 'on':
        #         Status=True
        # else:
        #     Status=False
        # print("status: "+ str(Status))
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
                return HttpResponse(json.dumps(resp), content_type="application/json")   
                # return HttpResponseRedirect('/department')  
                    
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
                # return HttpResponseRedirect('/department')
                return HttpResponse(json.dumps(resp), content_type="application/json")   
                # return department(request)
            
        except Exception as e:
            resp['status'] = 'failed'
            resp['msg']="Somehing went wrong!, please contact to system administrator..." + str(type(e))
            print(str(resp['msg']))
            print(e)
            return HttpResponse(json.dumps(resp), content_type="application/json")
        print('final')
        return HttpResponseRedirect("/department")
        # return department()
        # return render(request,'Employee/Department/Departments.html',{'msg':msg})
    # return HttpResponse(json.dumps(resp), content_type="application/json")
    else:
        return HttpResponse("<h1>404 - Page not found...")

# End Shift Views

# Assign Shift Views
def assign_shift(request):
    assign_shift_list = Employee_Shift_Master.objects.all()
    context = {
        'page_title':'Employee',
        'assign_shifts':assign_shift_list,
    }
    return render(request, 'Employee/Shift/Assign_Shift.html',context)

def manage_assign_shift(request):
    card_header=''
    assign_shift = {}
    data =  request.GET
    Emp_Active_List = Emp_Master.objects.filter(Emp_Status=True).all()
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
            card_header='Details of assigned shift: ' 

    if 'id' not in data and 'details' not in data:
        card_header='Assign Shift'

    context = {
        'assign_shift' : assign_shift,
        'employees' : Emp_Active_List,
        'shifts': Shift_Active_List,
        'card_header': card_header,
        'details' : details
    }
    return render(request, 'Employee/Shift/manage_assign_shift.html',context)


def delete_assign_shift(request):
    try:
        id = request.GET['id']
        Dept_Master.objects.filter(Dept_Id = id).delete()
        messages.warning(request, "Department id: "+str(id)+" Deleted successfully")
    except Exception as e:
        messages.error(request,"Somehing went wrong!, please contact to system administrator...")
    return HttpResponseRedirect("/department")

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

        try:
            Emp = Emp_Master.objects.filter(Emp_Id = Emp_Id).first()
            Shift = Shift_Master.objects.filter(Shift_Id =Shift_Id).first()

            # isExist = Emp_Master.isExists(Email_ID)
            # print(isExist)

            Emp_Shift_Id  = ''
            if 'Emp_Shift_Id' in data:
                Emp_Shift_Id = data['Emp_Shift_Id']
            print('id:'+Emp_Shift_Id)
            # print('test: ' not isExist)
            if Emp_Shift_Id == '':
                # if isExist == True:
                #     resp['status'] = 'failed'
                #     resp['msg']="Email id '"+Email_ID+"' is already exist, please use other Email id"
                #     print(str(resp['msg']))
                #     return HttpResponse(json.dumps(resp), content_type="application/json")
                
                save_Emp_Shift = Employee_Shift_Master(
                        Emp_Id=Emp,
                        Shift_Id=Shift,
                        Start_Date=Start_Date,
                        End_Date=End_Date
                    )
                save_Emp_Shift.save()
                messages.success(request, "Record added successfully")   
                resp['status'] = 'success'
                return HttpResponse(json.dumps(resp), content_type="application/json")   
                # return HttpResponseRedirect('/department')  
                    
            else:
                Employee_Shift_Master.objects.filter(Emp_Shift_Id = Emp_Shift_Id).update(
                    Emp_Id=Emp,
                    Shift_Id=Shift,
                    Start_Date=Start_Date,
                    End_Date=End_Date
                    )
                resp['status'] = 'success'
                messages.success(request, "Record updated successfully")  
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

# End Assign Shift Views
def shift_calender(request):
    assign_shift_list = Employee_Shift_Master.objects.all()
    context = {
        'page_title':'Employee',
        'assign_shifts':assign_shift_list,
    }
    return render(request, 'Employee/Shift/Shift_Calender.html',context)
# Shift Calender

# End Shift Calender