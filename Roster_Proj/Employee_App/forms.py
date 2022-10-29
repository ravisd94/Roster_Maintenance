from django.core import validators
from django import forms
from .models import Designation_Master

class RoleForm_Add(forms.ModelForm):
   class meta:
      model = Designation_Master
      fields=('Role_Name','Role_description','Role_Status')

