from pyexpat import model
from django.db import models
from datetime import datetime
from django.utils import timezone

from django.contrib.auth.models import AbstractUser
from .manager import UserManager


from PIL import Image
import qrcode
from io import BytesIO
from django.core.files.base import ContentFile

# Create your models here.

class Dept_Master(models.Model):
    Dept_Id=models.AutoField(primary_key=True)
    Dept_Name=models.CharField(max_length=100, unique = True) 
    Dept_description = models.TextField(null=True,blank=True)
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
    Desg_Name=models.CharField(max_length=100, blank=True,unique = True) 
    Desg_description = models.TextField(null=True,blank=True)
    Desg_Status=models.BooleanField(default=True)
    Dept_Id = models.ForeignKey(Dept_Master, on_delete=models.CASCADE)
    Created_By=models.IntegerField(null=True,blank=True)
    Created_Date=models.DateTimeField(default=timezone.now) 
    Modified_By=models.IntegerField(null=True,blank=True)
    Modified_Date=models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.Desg_Name

    def isExists(Name):
        if Designation_Master.objects.filter(Desg_Name = Name):
            return True
        return False
            
class Role_Master(models.Model):
    Role_Id=models.AutoField(primary_key=True)
    Role_Name=models.CharField(max_length=100, blank=True, unique = True) 
    Role_description = models.TextField(null=True,blank=True) 
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

class Project_Master(models.Model):
    Proj_id = models.AutoField(primary_key=True)
    Proj_Name=models.CharField(max_length=100, blank=True, unique = True)
    Proj_Description=models.TextField(null=True,blank=True)
    Client_Name =models.CharField(max_length=100, blank=True)
    Point_of_Contact_Name=models.CharField(max_length=100, blank=True)
    Point_of_Contact_Email=models.CharField(max_length=100, blank=True, unique = True)
    Proj_Start_Date=models.DateField(blank=True)
    Proj_End_Date=models.DateField(blank=True)
    Proj_Status=models.BooleanField(default=True)
    Proj_BarCode = models.ImageField(upload_to='images/')
    Created_By=models.IntegerField(null=True,blank=True)
    Created_Date=models.DateTimeField(default=timezone.now) 
    Modified_By=models.IntegerField(null=True,blank=True)
    Modified_Date=models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.Proj_Name
    
    def isExists(project):
        if Project_Master.objects.filter(Proj_Name = project):
            return True
        return False
    
    def save(self, *args, **kwargs):
        if not self.pk: # generate and save the QR code only if the object is being created for the first time
            # generate the QR code image
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(self.Proj_Name)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            # save the QR code image to a buffer
            buffer = BytesIO()
            img.save(buffer, format='PNG')
            self.Proj_BarCode.save(f'{self.Proj_Name}.png', ContentFile(buffer.getvalue()), save=False)
            super().save(*args, **kwargs)


class Emp_Master(AbstractUser):
    
    email= models.EmailField(unique=True, max_length=254, verbose_name='email address')
    username = None

    Emp_Id=models.AutoField(primary_key=True)
    Middle_Name=models.CharField(max_length=100, blank=True)
    Contact_Number= models.CharField(max_length=10, blank=True) 
    
    Dept_Id = models.ForeignKey(Dept_Master, on_delete=models.CASCADE,null=True)
    Desg_Id = models.ForeignKey(Designation_Master, on_delete=models.CASCADE,null=True)
    Role_Id=models.ForeignKey(Role_Master, on_delete=models.CASCADE,null=True)
    
    Project_Id= models.ForeignKey(Project_Master, on_delete=models.CASCADE,null=True)
    is_Project_Manager = models.BooleanField(default=False)

    Emp_Sex=models.CharField(max_length=100, blank=True)
    Birth_Date=models.DateField(blank=True,null=True)
    First_Login = models.BooleanField(default=True)
    Created_By=models.IntegerField(null=True,blank=True)
    Created_Date=models.DateTimeField(default=timezone.now) 
    Modified_By=models.IntegerField(null=True,blank=True)
    Modified_Date=models.DateTimeField(auto_now=True) 

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS=[]

    def __str__(self):
        return self.first_name + " " + self.Middle_Name + " " + self.last_name

    def isExists(email):
        if Emp_Master.objects.filter(email = email):
            return True
        return False
        
class Shift_Master(models.Model):
    Shift_Id=models.AutoField(primary_key=True)
    Shift_Name=models.CharField(max_length=100, unique = True)
    Shift_Start_Time=models.TimeField()
    Shift_End_Time=models.TimeField()
    Created_By=models.IntegerField(null=True,blank=True)
    Created_Date=models.DateTimeField(default=timezone.now) 
    Modified_By=models.IntegerField(null=True,blank=True)
    Modified_Date=models.DateTimeField(auto_now=True) 
    
    def __str__(self):
        return self.Shift_Name

    def isExists(Name):
        if Shift_Master.objects.filter(Shift_Name = Name):
            return True
        return False

class Employee_Shift_Master(models.Model):
    Emp_Shift_Id=models.AutoField(primary_key=True)
    Emp_Id=models.ForeignKey(Emp_Master, on_delete=models.CASCADE)
    Shift_Id=models.ForeignKey(Shift_Master, on_delete=models.CASCADE)
    Start_Date=models.DateField()
    End_Date=models.DateField()
    Shift_Start_Time=models.TimeField()
    Shift_End_Time=models.TimeField()
    Created_By=models.IntegerField(null=True,blank=True)
    Created_Date=models.DateTimeField(default=timezone.now) 
    Modified_By=models.IntegerField(null=True,blank=True)
    Modified_Date=models.DateTimeField(auto_now=True) 

class Attendance_Type(models.Model):
    Attendance_Type_Id=models.AutoField(primary_key=True)
    Attendance_Type_Name =models.CharField(max_length=100)
    Attendance_Type_Code =models.CharField(max_length=5)
    Attendance_Type_Description =models.CharField(max_length=200)
    Created_By=models.IntegerField(null=True,blank=True)
    Created_Date=models.DateTimeField(default=timezone.now) 
    Modified_By=models.IntegerField(null=True,blank=True)
    Modified_Date=models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.Attendance_Type_Name

class Attendance_Master(models.Model):
    Attendance_Id=models.AutoField(primary_key=True)
    Attendance_Type_Id=models.ForeignKey(Attendance_Type, on_delete=models.CASCADE)
    Emp_Id=models.ForeignKey(Emp_Master, on_delete=models.CASCADE)
    Emp_Shift_Id=models.ForeignKey(Employee_Shift_Master, on_delete=models.CASCADE)
    Attendance_Date=models.DateField()
    Clock_In_Time=models.TimeField(null=True,blank=True)
    Clock_Out_Time=models.TimeField(null=True,blank=True)
    Break_Start_Time=models.TimeField(null=True,blank=True)
    Break_End_Time=models.TimeField(null=True,blank=True)
    Created_By=models.IntegerField(null=True,blank=True)
    Created_Date=models.DateTimeField(default=timezone.now) 
    Modified_By=models.IntegerField(null=True,blank=True)
    Modified_Date=models.DateTimeField(auto_now=True) 

    def is_attendance_marked(Emp_Id,Attendance_Date):
        att_id = Attendance_Master.objects.filter(
            Emp_Id=Emp_Master.objects.filter(Emp_Id=Emp_Id).first(),
            Attendance_Date = Attendance_Date).first()
        if att_id:
            if att_id.Clock_In_Time != None and att_id.Clock_Out_Time != None:
                return ("Clocked in time: " + str(att_id.Clock_In_Time.strftime("%I:%M %p")) + 
                    " and Clocked out time: " + str(att_id.Clock_Out_Time.strftime("%I:%M %p"))),att_id.Attendance_Id
            elif att_id.Clock_In_Time != None:
                return "Marked Clock In",att_id.Attendance_Id
                
        return False

    def attendance_code(t):
        print('here')
        print(t)

        delta_hours = t.days * 24 + t.seconds / 3600.0
        print(delta_hours)
        if delta_hours < 4:
            return Attendance_Type.objects.filter(Attendance_Type_Code = 'A').first()
        elif delta_hours < 8 :
            return Attendance_Type.objects.filter(Attendance_Type_Code = 'HD').first()
        elif delta_hours >= 8 :
            return Attendance_Type.objects.filter(Attendance_Type_Code = 'P').first()
         # def is_Clocked_In(att_id):
    #     if Attendance_Master.objects.filter(Attendance_Id=att_id,Clock_In_Time__isnull=True):
    #         return False
    #     return True


