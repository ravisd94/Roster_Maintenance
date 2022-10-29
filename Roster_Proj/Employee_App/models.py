from pyexpat import model
from django.db import models
from datetime import datetime
from django.utils import timezone

# Create your models here.

class Dept_Master(models.Model):
    Dept_Id=models.AutoField(primary_key=True)
    Dept_Name=models.TextField(unique = True) 
    Dept_description = models.TextField() 
    Dept_Status=models.BooleanField(default=True)
    Created_By=models.IntegerField(null=True,blank=True)
    Created_Date=models.DateTimeField(default=timezone.now) 
    Modified_By=models.IntegerField(null=True,blank=True)
    Modified_Date=models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.Dept_Name
    
    def isExists(Name):
        if Dept_Master.objects.filter(Dept_Name = Name):
            return True
        return False

class Designation_Master(models.Model):
    Desg_Id=models.AutoField(primary_key=True)
    Desg_Name=models.TextField(unique = True) 
    Desg_description = models.TextField() 
    Desg_Status=models.BooleanField(default=True)
    Created_By=models.IntegerField(null=True,blank=True)
    Created_Date=models.DateTimeField(default=timezone.now) 
    Modified_By=models.IntegerField(null=True,blank=True)
    Modified_Date=models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.Designation_Name

    def isExists(Name):
        if Designation_Master.objects.filter(Desg_Name = Name):
            return True
        return False
            
class Role_Master(models.Model):
    Role_Id=models.AutoField(primary_key=True)
    Role_Name=models.TextField(unique = True) 
    Role_description = models.TextField() 
    Role_Status=models.BooleanField(default=True)
    Created_By=models.IntegerField(null=True,blank=True)
    Created_Date=models.DateTimeField(default=timezone.now) 
    Modified_By=models.IntegerField(null=True,blank=True)
    Modified_Date=models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.Role_Name

    def isExists(Name):
        if Role_Master.objects.filter(Role_Name = Name):
            return True
        return False

class Emp_Master(models.Model):
    Emp_Id=models.AutoField(primary_key=True)
    Email_ID=models.TextField(unique = True) 
    First_Name=models.TextField() 
    Middle_Name=models.TextField(blank=True)
    Last_Name=models.TextField()
    Dept_Id = models.ForeignKey(Dept_Master, on_delete=models.CASCADE)
    Contact_Number=models.IntegerField(blank=True)
    Joining_Date=models.DateField(blank=True)
    Desg_Id = models.ForeignKey(Designation_Master, on_delete=models.CASCADE)
    Job_Role=models.ForeignKey(Role_Master, on_delete=models.CASCADE)
    Emp_Sex=models.TextField(blank=True)
    Birth_Date=models.DateField(blank=True)
    Emp_Status=models.BooleanField(default=True)
    Created_By=models.IntegerField(null=True,blank=True)
    Created_Date=models.DateTimeField(default=timezone.now) 
    Modified_By=models.IntegerField(null=True,blank=True)
    Modified_Date=models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.First_Name +self.Middle_Name+self.Last_Name

    def isExists(email):
        if Emp_Master.objects.filter(Email_ID = email):
            return True
        return False
        
