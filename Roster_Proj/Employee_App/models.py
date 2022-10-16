from pyexpat import model
from django.db import models
from datetime import datetime
from django.utils import timezone

# Create your models here.

class Dept_Master(models.Model):
    Dept_Id=models.AutoField(primary_key=True)
    Dept_Name=models.TextField() 
    Dept_description = models.TextField() 
    Dept_Status=models.BooleanField(default=True)
    Created_By=models.IntegerField(null=True,blank=True)
    Created_Date=models.DateTimeField(default=timezone.now) 
    Modified_By=models.IntegerField(null=True,blank=True)
    Modified_Date=models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.Dept_Name

class Designation_Master(models.Model):
    Desg_Id=models.AutoField(primary_key=True)
    Desg_Name=models.TextField() 
    Desg_description = models.TextField() 
    Desg_Is_Active=models.BooleanField(default=True)
    Created_By=models.IntegerField(null=True,blank=True)
    Created_Date=models.DateTimeField(default=timezone.now) 
    Modified_By=models.IntegerField(null=True,blank=True)
    Modified_Date=models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.Designation_Name

class Emp_Master(models.Model):
    Emp_Id=models.AutoField(primary_key=True)
    Email_ID=models.TextField() 
    First_Name=models.TextField() 
    Middle_Name=models.TextField(blank=True)
    Last_Name=models.TextField()
    Dept_Id = models.ForeignKey(Dept_Master, on_delete=models.CASCADE)
    Contact_Number=models.IntegerField(blank=True)
    Joining_Date=models.DateTimeField(blank=True)
    Desg_Id = models.ForeignKey(Designation_Master, on_delete=models.CASCADE)
    Job_Role=models.CharField(max_length=10,blank=True)
    Emp_Sex=models.TextField(blank=True)
    Birth_Date=models.DateField(blank=True)
    Is_Active=models.BooleanField(default=True)
    Created_By=models.IntegerField(null=True,blank=True)
    Created_Date=models.DateTimeField(default=timezone.now) 
    Modified_By=models.IntegerField(null=True,blank=True)
    Modified_Date=models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.First_Name +self.Middle_Name+self.Last_Name
