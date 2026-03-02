from django.shortcuts import render,redirect
from .models import Employee
from .models import Department
from .models import EmpQuery
from django .contrib import messages
from django.core.mail import send_mail


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
         employee = Employee.objects.filter(Email=e)
         if employee:
            emp_data = Employee.objects.get(Email=e)
            if p == emp_data.Code:
               req.session['emp_id'] = emp_data.id
               return redirect('employeedashboard')
            else:
               messages.warning(req,'email & password not match')
               return redirect('login')
         else:
           messages.warning(req,'Employee not exist in our company')
           return redirect('login')
         #   user = Employee.objects.filter(Email=e)
         # if not user:
         #    msg = "Register first"
         #    return redirect('Registration',{'Rmsg':msg})
         # else:
         #    userdata = Employee.objects.get(Email=e)
         #    if p == userdata.Password:
         #       req.session['user_id']=userdata.id
         #       return redirect('userdashboard')
         #    else:
         #       msg = 'Email & password not match'
         #       return render(req,'login.html',{'x':msg}) 
  return render(req,'login.html')
     



def employeedashboard(req):
   if 'emp_id' in req.session:
      eid = req.session.get('emp_id')
      emp_data = Employee.objects.get(id=eid)
      return render(req,'employeedashboard.html',{'data':emp_data})
   return redirect(login)


def admindashboard(req):
   if 'a_data' in req.session:
      a_data = req.session.get('a_data')
      return render(req,'admindashboard.html',{'data':a_data})
   return redirect('login')

def add_dept(req):
   if 'a_data'in req.session:
      a_data = req.session.get('a_data')
      return render(req,'admindashboard.html',{'data':a_data, 'add_dep':True})
   else:
      return redirect('login')
   
def show_dept(req):
   if 'a_data'in req.session:
      a_data = req.session.get('a_data')
      all_dept = Department.objects.all()
      return render(req,'admindashboard.html',{'data':a_data, 'show_dep':True,'all_dept':all_dept})
   else:
      return redirect('login')

def save_dept(req):
   if 'a_data' in req.session:
      if req.method == 'POST':
         dn = req.POST.get('dep_name')
         dd = req.POST.get('dep_desc')
         dh = req.POST.get('dep_head')
         dept = Department.objects.filter(Dep_n=dn)
         if dept:
            messages.warning(req,'Department already exist')
            a_data = req.session.get('a_data')
            return render(req,'admindashboard.html',{'data':a_data , 'add_dep':True})
         else:
            Department.objects.create(Dep_n=dn,Dep_d=dd,Dep_h=dh)
            messages.success(req, "Department Created")
            a_data = req.session.get('a_data')
            return render(req, 'admindashboard.html',{'data':a_data , 'add_dep':True})
   else:
      return redirect('login')


def add_emp(req):
   if 'a_data'in req.session:
         a_data = req.session.get('a_data')
         all_dept = Department.objects.all()
         return render(req,'admindashboard.html',{'data':a_data, 'add_emp':True , 'all_dept':all_dept})
   else:
      return redirect('login')

def save_emp(req):
   if 'a_data' in req.session:
      if req.method == 'POST':
         en = req.POST.get('emp_name')
         ee = req.POST.get('emp_email')
         ec = req.POST.get('emp_contact')
         ed = req.POST.get('emp_dept')
         ecode = req.POST.get('emp_code')
         ei = req.FILES.get('emp_image')
         emp = Employee.objects.filter(Email=ee)
         if emp:
            messages.warning(req,'email already exist')
            a_data = req.session.get('a_data')
            all_dept = Department.objects.all()
            return render(req,'admindashboard.html',{'data':a_data,'add_emp':True,'all_dept':all_dept})
         else:
            Employee.objects.create(Name=en,Email=ee,Contact=ec,Image=ei,Code=ecode,Dept=ed)
            send_mail('email from admin',
                              f'Employee information is Name:{en},Email:{ee},Contact:{ec},Department:{ed},Code:{ecode}',
                              'sharvan70458@gmail.com',
                              [ee],
                              fail_silently=False,)
            messages.success(req, "Employee Created")
            a_data = req.session.get('a_data')
            all_dept = Department.objects.all()
            return render(req, 'admindashboard.html',{'data':a_data , 'add_emp':True , 'all_dept':all_dept})
   else:
      return redirect('login')

def show_emp(req):
   if 'a_data'in req.session:
      a_data = req.session.get('a_data')
      all_emp = Employee.objects.all()
      return render(req,'admindashboard.html',{'data':a_data, 'show_emp':True,'all_emp':all_emp})
   else:
      return redirect('login')

def emp_all_Query(req):
   if 'a_data'in req.session:
      a_data = req.session.get('a_data')
      emp_all_Query = EmpQuery.objects.all()
      return render(req,'admindashboard.html',{'data':a_data , 'emp_all_Query':True, 'emp_all_Query':emp_all_Query})
   return redirect('login')


def reply(req,pk):
   if 'a_data' in req.session:
      q_data = EmpQuery.objects.get(id=pk)
      emp_all_Query = EmpQuery.objects.all()
      return render(req,'admindashboard.html',{'q_data':q_data , 'emp_all_Query':emp_all_Query,})
   return redirect('login')

def a_reply(req,pk):
   if 'a_data' in req.session:
      q_old_data=EmpQuery.objects.get(id=pk)
      if req.method=='POST':
         ar=req.POST.get('reply')
         q_old_data.Reply=ar
         q_old_data.Status="Done"
         q_old_data.save()
      a_data=req.session.get('a_data')
      emp_all_query=EmpQuery.objects.all()
      return render(req,'admindashboard.html',{'a_data':a_data,'emp_all_query':emp_all_query})
   return redirect('login')

def cancel(req):
   return redirect('emp_all_Query')
   

def profile(req):
   if 'emp_id' in req.session:
      eid = req.session.get('emp_id')
      emp_data = Employee.objects.get(id=eid)
      return render(req,'employeedashboard.html',{'data':emp_data , 'profile':True})
   return redirect('login')

def setting(req):
   if 'emp_id' in req.session:
      eid = req.session.get('emp_id')
      emp_data = Employee.objects.get(id=eid)
      return render(req,'employeedashboard.html',{'data':emp_data , 'setting':True})
   return redirect('login')

def Query(req):
   if 'emp_id' in req.session:
      eid = req.session.get('emp_id')
      emp_data = Employee.objects.get(id=eid)
      emp_dept = Department.objects.all()
      return render(req,'employeedashboard.html',{'data':emp_data , 'Query':True,'emp_dept':emp_dept})
   return redirect('login')

def edit(req):
   return render(req,'edit.html')

def reset(req):
   if 'emp_id' in req.session:
      if req.method == 'POST':
         eid = req.session.get('emp_id')
         image = req.FILES.get('img')
         emp_data = Employee.objects.get(id=eid)
         emp_data.Image = image
         print(emp_data.Image)
         emp_data.save()
         print(emp_data.Image)
         messages.success(req,'images change succesful')
         return redirect('profile')
      else:
         return render(req,'edit.html')
   return render(req,'login.html')

def querydata(req):
   if req.method == 'POST':
      if 'emp_id' in req.session:
         n = req.POST.get('name')
         e = req.POST.get('email')
         d = req.POST.get('Qdept')
         q = req.POST.get('query')
         EmpQuery.objects.create(Name=n,Email=e,Dept=d,Query=q)
         messages.success(req,"Query Created")
         eid = req.session.get('emp_id')
         emp_data = Employee.objects.get(id=eid)
         emp_dept = Department.objects.all()
         return render(req,'employeedashboard.html',{'data':emp_data ,'Query':True,'emp_dept':emp_dept})
      else:
         return redirect('employeedashboard') 
   return redirect('login') 
   
     

def all_Query(req):
   if 'emp_id' in req.session:
      eid = req.session.get('emp_id')
      emp_data = Employee.objects.get(id=eid)
      all_Query = EmpQuery.objects.filter(Email=emp_data.Email)
      return render(req,'employeedashboard.html',{'data':emp_data , 'all_Query':True, 'all_Query':all_Query,})
   return redirect('login')

def pending_Query(req):
   if 'emp_id' in req.session:
      eid = req.session.get('emp_id')
      emp_data = Employee.objects.get(id=eid)
      pending_data = EmpQuery.objects.filter(Email=emp_data.Email,Status="pending")
      # all_Query = EmpQuery.objects.filter(Email=emp_data.Email)
      return render(req,'employeedashboard.html',{'data':emp_data,'pending_Query':True, 'pending_data':pending_data})
   return redirect('login')

def done_Query(req):
   if 'emp_id' in req.session:
      eid = req.session.get('emp_id')
      emp_data = Employee.objects.get(id=eid)
      d_Query = EmpQuery.objects.filter(Email=emp_data.Email,Status="Done")
      return render(req,'employeedashboard.html',{'data':emp_data , 'done_Query':True, 'd_Query':d_Query})
   return redirect('login')

def emp_edit(req,pk):
   if 'emp_id' in req.session:
      edit_data = EmpQuery.objects.get(id=pk)
      eid = req.session.get('emp_id')
      emp_data = Employee.objects.get(id=eid)
      all_Query = EmpQuery.objects.filter(Email=emp_data.Email)
      return render(req,'employeedashboard.html',{'data':emp_data,'all_Query':all_Query,'edit_data':edit_data})
   return redirect('login')

def update(req,pk):
   if 'emp_id' in req.session:
      eid=req.session.get('emp_id')
      emp_data = Employee.objects.get(id=eid)
      if req.method=='POST':
         n=req.POST.get('name')
         d=req.POST.get('dept')
         q=req.POST.get('query')
         e_old_data=EmpQuery.objects.get(id=pk)
         e_old_data.Name=n
         e_old_data.Dept=d
         e_old_data.Query=q
         e_old_data.save()
      all_Query=EmpQuery.objects.all()
      return render(req,'employeedashboard.html',{'data':emp_data,'all_Query':all_Query})
   return redirect('login')

def search(req):
   if 'emp_id' in req.session:
      eid = req.session.get('emp_id')
      emp_data = Employee.objects.get(id=eid)
      if req.method == 'POST':
         s= req.POST.get('search')
         # all_Query = EmpQuery.objects.filter(Email=emp_data.Email,Query=s, Dept=s)
         all_Query = EmpQuery.objects.filter(Email=emp_data.Email,Query=s)
         # all_Query = EmpQuery.objects.filter(Email__contains=emp_data.Email,Query__icontains=s)
      return render(req,'employeedashboard.html',{'data':emp_data,'all_Query':all_Query,})
   return redirect('login')

        
      

def delete(req, pk):
    if 'emp_id' in req.session:
        delete_data = EmpQuery.objects.get(id=pk)
        delete_data.delete()
        return redirect('all_Query')
    return redirect('login')

def logout(req):
   if 'user_id' in req.session:
      req.session.flush()
      return redirect('login')
   return redirect('login')


