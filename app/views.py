from django.shortcuts import render,redirect
from .models import Employee

# Create your views here.


def landing(req):
    return render(req , 'landing.html')

def registration(req):
   if req.method == 'POST':
        n=req.POST.get('name')
        e=req.POST.get('email')
        c=req.POST.get('number')
        p = req.POST.get('password')
        q = req.POST.getlist('qualification')
        g= req.POST.get('gender')
        s= req.POST.get('state')
    
        Employee.objects.create(
            Name = n,
            Email = e, 
            Password = p,
            Contact = c,
            Qualification = q,
            Gender = g,
            State = s
        )
        return redirect('login')
   
   return render(req,'Registration.html')

def login(req):
    return render(req,'login.html')
