from django.shortcuts import render, redirect 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import  CreateUserForm
from BloodB.models import PERSON,DONATION,donates,RECEIVE,receives,STOCK
from datetime import datetime ,date
from django.utils import timezone

# Create your views here.

@login_required
def home(request):
    return render(request,'home.html')

@login_required
def success(request):
    return render(request,'success.html')

@login_required
def decline(request):
    return render(request,'decline.html')

@login_required
def Pid(request,role):
	if request.method=="POST" :
		cond1=request.POST.get('pid')
		print("PID=",cond1)
		print(len(PERSON.objects.filter(pid=int(cond1))))
		cond2=len(PERSON.objects.filter(pid=int(cond1)))
		
		if cond2!=0  :
			context={
				"pid":cond1,
				"bgroup":PERSON.objects.get(pid=int(cond1)).bgroup
			}
			if role=="donor":
				return render(request,'donateform.html',context)
			else:
				return render(request,'receive.html',context)
		elif  cond1!="0" and  cond2==1:
			context={
				"pid":cond1,
				"bgroup":PERSON.objects.get(pid=int(cond1)).bgroup
			}
			if role=="donor":
				return render(request,'donateform.html',context)
			else:
				return render(request,'receive.html',context)
		else:
			message={'msg1' : "Invalid ID !","role":role}
			return render(request,'Pid.html',message)
	return render(request,'Pid.html',{"role":role})

		
@login_required
def donate(request):
	if request.method=="POST" :
		# did=len(DONATION.objects.all())+1
		pid = request.POST.get('pid')
		dqty = request.POST.get('dqty')
		donate=DONATION(ddate=datetime.today(),dqty=dqty)
		donate.save();
		pidd=PERSON.objects.get(pid=pid);
		didd=DONATION.objects.last();
		did=str(DONATION.objects.last().did)
		donate=donates(pid=pidd,did=didd)
		donate.save();
		quantity=STOCK.objects.get(sbgroup=PERSON.objects.get(pid=pid).bgroup).qty
		STOCK.objects.filter(sbgroup=PERSON.objects.get(pid=pid).bgroup).update(qty=quantity+int(dqty))
		
		dids=DONATION.objects.filter(did=did)
		params={
			"id":dids,
			"msg":"Donation Id"
		}
		# print(params)
	return render(request,'success.html',params)

@login_required
def registration(request,role):
	if request.method=="POST" :
		fname = request.POST.get('fname')
		lname=request.POST.get('lname')
		gender=request.POST.get('gender')
		dob=request.POST.get('dob')
		curage=int(request.POST.get('age'))
		phone=request.POST.get('phone')
		address=request.POST.get('address')
		bgroup=request.POST.get('bloodgroup')
		MIssues= request.POST.get('med')
		donate=PERSON(fname=fname,lname=lname,gender=gender,dob=dob,
		phone=phone,address=address,bgroup=bgroup,MIssues=MIssues)
		donate.save();
		id=str(PERSON.objects.last().pid)
		age=calculate_age(dob)
		print("AGE=",age)
		piddict={
			"pid":id,
			"age":age,
			"bgroup":bgroup
		}
		params={
			'msg1':"Registered Successfully",
			'msg2':"Person ID = "+str(id)
		}
		if role=="donor":
			return render(request,'donateform.html',piddict)
		elif role=="receiver":
			return render(request,'receive.html',piddict)
		else:
			return render(request,'success.html',params)
		
	return render(request,'registration.html',{"role":role})

@login_required
def donateform(request):
	if request.method=="POST" :
		pid = request.POST.get('pid')
		age=int(request.POST.get('age'))
		MIssues= request.POST.get('med')
		Weight= int(request.POST.get('weight'))
		Hb= int(request.POST.get('hb'))
		BPd= int(request.POST.get('bpd'))
		BPs= int(request.POST.get('bps'))
		temp= int(request.POST.get('temp'))
		Pulse=int(request.POST.get('pulse'))
		Cond=int(request.POST.get('condition'))
		
		if Weight <= 45 or Hb<=12.5 or BPd<50 or  BPd>100 or BPs<100 or  BPs>180 or Pulse<50 or Pulse>100 or age<18 or age>60 or temp>37.5 :
			params={
				"msg":"You're not eligible to donate"
			}
			return render(request,'decline.html',params)
		elif Cond==0 or Cond==14:
			piddict={
			"pid":pid
			}
			return render(request,'donate.html',piddict)
			
		else:
			params={
				"msg":"You're not eligible to donate"
			}
			return render(request,'decline.html',params)
			
	return render(request,'donateform.html')

@login_required
def receiveform(request):

		if request.method=="POST" :
			# pid=len(PERSON.objects.all())+1
			fname = request.POST.get('fname')
			lname=request.POST.get('lname')
			gender=request.POST.get('gender')
			dob=request.POST.get('dob')
			phone=request.POST.get('phone')
			address=request.POST.get('address')
			bgroup=request.POST.get('bloodgroup')
			MIssues= request.POST.get('med')
			receiveform=PERSON(fname=fname,lname=lname,gender=gender,dob=dob,
			phone=phone,address=address,bgroup=bgroup,MIssues=MIssues)
			receiveform.save();
			pid=str(PERSON.objects.last().pid);
			piddict={
				"pid":pid,
				"bgroup":bgroup
			}
			return render(request,'receive.html',piddict)	
		return render(request,'receiveform.html')	
		
		

@login_required
def receive(request):
	
	if request.method=="POST" :
		pid=request.POST.get('pid')
		# rid=len(RECEIVE.objects.all())+1
		rqty = request.POST.get('rqty')
		hospital_name=request.POST.get('hospital_name')
		# print(hospital_name)
		rbgroup=request.POST.get('rbgroup')

		quantity=STOCK.objects.get(sbgroup=PERSON.objects.get(pid=pid).bgroup).qty
		if int(rqty) > quantity:
			params={
				"msg":"Insufficent Stock"
			}
			return render(request,'decline.html',params)

		receive=RECEIVE(rdate=datetime.today(),rqty=rqty,hospital_name=hospital_name,rbgroup=rbgroup)
		receive.save();
		pidd=PERSON.objects.get(pid=pid);
		ridd=RECEIVE.objects.last();
		rid=str(RECEIVE.objects.last().rid);
		receive=receives(pid=pidd,rid=ridd)
		receive.save();
		
		# quantity=STOCK.objects.get(sbgroup=PERSON.objects.get(pid=pid).bgroup).qty
		STOCK.objects.filter(sbgroup=PERSON.objects.get(pid=pid).bgroup).update(qty=quantity-int(rqty))

		rids=RECEIVE.objects.filter(rid=rid)
		params={
			"id":rids,
			"msg":"Receiver Id  "
		}
		
		
		return render(request,'success.html',params)
	
	
@login_required
def stock(request):
	qty=STOCK.objects.all();
	params={
		"obj":qty
	}
	return render(request,'stock.html',params)

@login_required
def search(request):
	if request.method == 'POST':
		search=request.POST.get("search")
		q1=PERSON.objects.filter(pid=search)
		q2=donates.objects.filter(pid=search)
		
		list1=[]
		for i in q2:
			list1.append(i.did.did)
		# print(list)
		q3=DONATION.objects.filter(did__in=list1)
		# print(q3)
		q4=receives.objects.filter(pid=search)
		print(q4)
		list2=[]
		for i in q4:
			list2.append(i.rid.rid)
		print(list2)
		q5=RECEIVE.objects.filter(rid__in=list2)
		cond1=len(q1)
		cond2=len(q3)
		cond3=len(q5)
		if cond1==0 :
			params={
				'msg':"Invalid ID !"
			}
			return render(request,'search.html',params)
		
		elif cond2==0 and cond3==0:
			params={
			'obj1':q1,
			"msg1":["----------","No Donations Yet","----------"],
			"msg2":["----------","Never received blood","----------"]
			}
			return render(request,'displaydetails.html',params)
		elif cond2!=0 and cond3==0:
			params={
			'obj1':q1,
			'obj2':q3,
			"msg2":["----------","Never received blood","----------"]
			}
			return render(request,'displaydetails.html',params)
	
		elif cond2==0 and cond3!=0:
			params={
				'obj1':q1,
				'obj3':q5,
				"msg1":["----------","No Donations Yet","----------"],
			}
			return render(request,'displaydetails.html',params)
		elif cond2!=0 and cond3!=0:
			params={
				'obj1':q1,
				'obj2':q3,
				'obj3':q5,
				}
			return render(request,'displaydetails.html',params)
	return render(request,'search.html')

@login_required
def displaydetails(request):
	return render(request,'displaydetails.html')

@login_required
def updatedetails(request,id):
	if request.method=="POST" :
		fname = request.POST.get('fname')
		lname=request.POST.get('lname')
		gender=request.POST.get('gender')
		dob=request.POST.get('dob')
		phone=request.POST.get('phone')
		address=request.POST.get('address')
		bgroup=request.POST.get('bloodgroup')
		PERSON.objects.filter(pid=id).update(fname=fname,lname=lname,gender=gender,dob=dob,phone=phone,address=address,bgroup=bgroup)
		params={
			'msg1':"Successfully Updated Person Details",
			'msg2':"Person ID = "+str(id)
		}
		return render(request,'success.html',params)
	context={"obj":PERSON.objects.filter(pid=id)}
	return render(request,'updatedetails.html',context)

@login_required
def deleteperson(request):
	if request.method == "POST":
		delpid=request.POST.get("pid")
		PERSON.objects.filter(pid=delpid).delete()
		params={
			'msg1':"Successfully Deteted One Person",
			'msg2':"Person ID = "+str(delpid)
		}
		return render(request,'success.html',params)


def registerUser(request):

	if request.user.is_authenticated:
		return redirect('home')
	else:
		form = CreateUserForm()
		if request.method == 'POST':
			form = CreateUserForm(request.POST)
			if form.is_valid():
				form.save()
				user = form.cleaned_data.get('username')
				messages.success(request, 'Account Created for ' + user)

				return redirect('/login')
			

		context = {'form':form}
		return render(request, 'register.html', context)


def loginUser(request):
	if request.user.is_authenticated:
		return redirect('/home')
	else:
		if request.method == 'POST':
			username = request.POST.get('username')
			password =request.POST.get('password')
			
			user = authenticate(request, username=username, password=password)

			if user is not None:
				login(request, user)
				return redirect('/home')
			else:
				messages.info(request, 'Username OR password is incorrect')

		
		return render(request, 'login.html')


def logoutUser(request):
	logout(request)
	return redirect('/login')

def calculate_age(born):
    today = date.today()
    return today.year - int(born[0:4]) - ((today.month, today.day) < (int(born[5:7]), int(born[8:10])))