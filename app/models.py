from django.db import models

# Create your models here.


class Employee(models.Model):
    Name = models.CharField(max_length=50)
    Email= models.EmailField()
    Contact = models.IntegerField()
    Image= models.ImageField(upload_to='image',null=True)
    Code = models.CharField(max_length=50)
    Dept=models.CharField(max_length=20)

  
class Department(models.Model):
    Dep_n= models.CharField(max_length=30)
    Dep_d= models.CharField(max_length=100)
    Dep_h=models.CharField(max_length=30)