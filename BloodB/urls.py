"""DBMS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from BloodB import views

urlpatterns = [
    
    path('admin/', admin.site.urls),
    path('',views.loginUser,name='login'),
    path('home',views.home,name='home'),
    path('registration/<str:role>',views.registration,name='registration'),
    path('Pid/<str:role>',views.Pid,name='Pid'),
    path('success',views.success,name='success'),
    path('decline',views.decline,name='decline'),
    path('donateform',views.donateform,name='donateform'),
    path('donate',views.donate,name='donate'),
    path('receive',views.receive,name='receive'),
    path('search',views.search,name='search'),
    path('displaydetails',views.displaydetails,name='displaydetails'),
    path('update/<int:id>',views.updatedetails,name='updatedetails'),
    path('deleteperson',views.deleteperson,name='deleteperson'),
    path('stock',views.stock,name='stock'),
    path('login',views.loginUser,name='login'),
    path('register',views.registerUser,name='register'),
    path('logout/',views.logoutUser,name='logout')

]
