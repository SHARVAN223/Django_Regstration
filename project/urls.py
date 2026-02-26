"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from app.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', landing, name='landing'),
    path('registration/',registration , name='registration'),
    path('login/',login,name='login'),
    # path('userdashboard/', userdashboard, name='userdashboard'),
    path('admindashboard/',admindashboard, name='admindashboard'),
    path('add_dept/',add_dept,name='add_dept'),
    path('show_dept/',show_dept,name='show_dept'),
    path('save_dept/',save_dept,name='save_dept'),
    path('add_emp/',add_emp,name='add_emp'),
    path('show_emp/',show_emp,name='show_emp'),
    path('save_emp/',save_emp,name='save_emp'),
    path('employeedashboard/',employeedashboard,name='employeedashboard'),
    path('profile/',profile,name='profile'),
    path('setting/',setting,name='setting'),
    path('Query/',Query,name='Query'),
    path('edit/',edit,name='edit'),
    path('reset/',reset,name='reset'),
    path('querydata/',querydata,name='querydata'),
    path('all_Query/',all_Query,name='all_Query'),
    path('pending_Query/',pending_Query,name='pending_Query'),
    path('done_Query/',done_Query,name='done_Query'),
    path('emp_all_Query/',emp_all_Query,name='emp_all_Query'),
    # path('emp_all_query/reply/<int:pk/',reply,name='reply'),
    path('reply/',reply,name='reply'),
    path('logout/',logout,name='logout'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
