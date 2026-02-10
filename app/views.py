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
        cp = req.POST.get('cpassword')
        q = req.POST.getlist('qualification')
        g= req.POST.get('gender')
        s= req.POST.get('state')
        user = Employee.objects.filter(Email=e)
        if user :
          msg="Email id already exists!"
          return render(req,'Registration.html',{'Emsg':msg})
        else:
          if p==cp:    
              Employee.objects.create(
                Name = n,
                Email = e, 
                Password = p,
                Cpassword=cp,
                Contact = c,
                Qualification = q,
                Gender = g,
                State = s
              )
              return redirect('login')
          else:
              userdata={'name':n,'email':e,'number':c}
              msg="Password & Confirm_password not matched"
              return render(req,'Registration.html',{'pmsg':msg,'data':userdata})
   return render(req,'Registration.html')

def login(req):
    return render(req,'login.html')
