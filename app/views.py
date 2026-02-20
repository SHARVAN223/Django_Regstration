from django.shortcuts import render,redirect
from .models import Employee
from .models import Department
from django .contrib import messages

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
  if req.method == 'POST':
     e = req.POST.get('email')
     p =req.POST.get('password')
     if e=='admin@gmail.com' and p=='admin':
            a_data={
                'id':1,
                'name':'Admin',
                'email':'admin@gmail.com',
                'password':'admin'
            }
            req.session['a_data']=a_data
            return redirect('admindashboard')
     else:
         user = Employee.objects.filter(Email=e)
         if not user:
            msg = "Register first"
            return redirect('Registration',{'Rmsg':msg})
         else:
            userdata = Employee.objects.get(Email=e)
            if p == userdata.Password:
               req.session['user_id']=userdata.id
               return redirect('userdashboard')
            else:
               msg = 'Email & password not match'
               return render(req,'login.html',{'x':msg})
  return render(req,'login.html')
     

def userdashboard(req):
   if 'user_id' in req.session:
      id = req.session.get('user_id')
      userdata = Employee.objects.get(id = id)
      return render(req, 'userdashboard.html',{'data':userdata})
   return redirect('login')  


def admindashboard(req):
   if 'a_data' in req.session:
      a_data = req.session.get('a_data')
      return render(req,'admindashboard.html',{'data':a_data})


def add_dept(req):
   if 'a_data'in req.session:
      a_data = req.session.get('a_data')
      return render(req,'admindashboard.html',{'data':a_data, 'add_dep':True})
   else:
      return redirect('login')
   
def show_dept(req):
   if 'a_data'in req.session:
      a_data = req.session.get('a_data')
      return render(req,'admindashboard.html',{'data':a_data, 'show_dep':True})
   else:
      return redirect('login')

def save_dept(req):
   if 'a_data' in req.session:
      if req.method == 'POST':
         dn = req.POST.get('dep_name')
         dd = req.POST.get('dep_desc')
         dh = req.POST.get('dep_head')
         dept = Department.objects.filter(Dep_name=dn)
         if dept:
            messages.warning(req,'Department already exist')
            a_data = req.session.get('a_data')
            return render(req,'admindashboard.html',{'data':a_data , 'add_dep':True})
         else:
            Department.objects.create(Dep_name=dn,Dep_desc=dd,Dep_head=dh)
            messages.success(req, "Department Created")
            a_data = req.session.get('a_data')
            return render(req, 'admindashboard.html',{'data':a_data , 'add_dep':True})
   else:
      return redirect('login')


def logout(req):
   if 'user_id' in req.session:
      req.session.flush()
      return redirect('login')
   return redirect('login')


