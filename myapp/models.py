from django.db import models

# Create your models here.


class LoginDetails(models.Model):
    login_date = models.DateTimeField(blank=False)
    Emp_code = models.CharField(max_length=10,blank=False)
    emp_name = models.CharField(max_length=100)
    company = models.CharField(max_length=50)
    department = models.CharField(max_length=50)
