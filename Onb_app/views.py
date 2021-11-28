from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotFound
from .forms import UserRegisterForm
from django.contrib import messages
from .models import *
from django.contrib.auth.models import User
import datetime


# Create your views here.

def test(request):
	return render(request, 'test.html')


@login_required(login_url='/login/')
def register(request):
	u = User.objects.get(username=request.user.username)
	if u.profile.role=="MANAGER" or request.user.is_superuser:
	    form = UserRegisterForm(request.POST)
	    if request.method == 'POST':
		    if form.is_valid():
		        user = form.save()
		        user.refresh_from_db()
		        user.profile.firstname = form.cleaned_data.get('firstname')
		        user.profile.lastname = form.cleaned_data.get('lastname')
		        user.profile.email = form.cleaned_data.get('email')
		        user.profile.role = form.cleaned_data.get('role')
		        user.profile.startdate = form.cleaned_data.get('startdate')
		        user.profile.enddate = form.cleaned_data.get('enddate')
		        user.save()
		        messages.success(request, "User creation successful!")
		        return redirect('/register/')
		    else:
		        return render(request, 'register.html', {'form': form, 'title': 'Register Users'})
	    else:
    		form = UserRegisterForm()
    		return render(request, 'register.html', {'form': form, 'title': 'Register Users'})
	else:
		logout(request)
		messages.error(request, "Your account does not have sufficient privileges to perform this action. If you think this is an error, please contact your manager.")
		return redirect('/error/')


def auth_login(request):
	if request.user.is_authenticated:
		return redirect('/welcome/')
	else:
		return render(request, 'login.html', {'title': 'Login'})


def logincheck(request):
	logout(request)
	username = password = ''
	if request.POST:
	    username = request.POST['username']
	    password = request.POST['password']

	    user = authenticate(request, username=username, password=password)
	    if user is not None:
	        if user.is_active:
	            login(request, user)
	            return HttpResponseRedirect('/welcome/')
	        else:
	        	messages.error(request, "Your account is not active, please contact your manager!")
	        	return redirect('/login/')
	    else:
	    	messages.error(request, "Invalid Credentials, please try again!")
	    	return redirect('/login/')
	return render(request, "login.html")


def auth_logout(request):
    logout(request)
    return redirect('/login/')


def error(request):
	return render(request, 'error.html')


@login_required(login_url='/login/')
def welcome(request):
	user = User.objects.get(username=request.user.username)
	'''return render(request, 'welcome.html', {'title': 'Welcome', 'user':user})
	'''
	if user.profile.firstlogin:
		user.profile.firstlogin = False
		user.save()
		return render(request, 'welcome.html', {'title': 'Welcome', 'user':user})
	else:
		return HttpResponseRedirect('/home/')


@login_required(login_url='/login/')
def profile_page(request):
		prof = User.objects.get(username=request.user.username)
		return render(request, 'profile_page.html', {'prof':prof})


@login_required(login_url='/login')
def updateprofile(request):
	if request.method == 'POST':
		firstname = request.POST['firstname']
		lastname = request.POST['lastname']
		user = User.objects.get(username=request.user.username)
		user.profile.firstname = firstname
		user.profile.lastname = lastname
		user.save()
		print(firstname, lastname)
		return HttpResponse('')

	
@login_required(login_url='/login/')
def home(request):
	prof = User.objects.get(username=request.user.username)
	try:
		onb = onboarding.objects.get(newhire=request.user.username)
		nh_week = newhire_weeks.objects.filter(onboarding=onb)
		perc = newhire_weeks.objects.filter(onboarding=onb, status=True)
		usr = User.objects.all()
		return render(request, 'home.html', {'title': 'Onboarding Home', 'prof':prof, 'perc': perc, 'onb':onb, 'usr':usr, 'nh_week':nh_week})
	except:
		onb = None
		perc = 0
		return render(request, 'home.html', {'title': 'Onboarding Home', 'prof':prof, 'perc': perc, 'onb':onb})


@login_required(login_url='/login/')
def viewsupportengineers(request):
	if request.user.profile.role=="MANAGER" or request.user.is_superuser:
		eng = Profile.objects.filter(role='ENGINEER')
		manager = Profile.objects.filter(role='MANAGER')
		nh = Profile.objects.filter(role='NEW_HIRE')
		onb = onboarding.objects.all()
		usr = User.objects.all()
		return render(request, 'userpage.html', {'eng': eng, 'manager':manager, 'nh':nh, 'onb':onb, 'usr':usr})
	else:
		logout(request)
		messages.error(request, "Your account does not have sufficient privileges to perform this action. If you think this is an error, please contact your manager.")
		return redirect('/error/')


@login_required(login_url='/login/')
def onb_assign(request):
	if request.user.profile.role=="MANAGER" or request.user.is_superuser:
		if request.method == 'POST':
			new_hire = request.POST['new_hire']
			trail_guide = request.POST['trail_guide']
			onb_buddy = request.POST['onb_buddy']
			the_manager = request.POST['the_manager']
			onb = onboarding.objects.filter(newhire=new_hire)
			if not onb:
				onb = onboarding(newhire = new_hire, trailguide = trail_guide, onboardingbuddy = onb_buddy, the_manager=the_manager)
				onb.save()
				weeks = weeks_data.objects.all()
				for w in weeks:
					wno = newhire_weeks.objects.create(onboarding=onb, weekid=w.weekid, weektitle=w.weektitle)
					c = content.objects.filter(weeks_data=w)
					for c in c:
						newhire_content.objects.create(newhire_weeks=wno, task_id=c.task_id, task=c.task)
				target = targets.objects.all()
				for t in target:
					newhire_targets.objects.create(onboarding=onb, target_id=t.target_id, target=t.target)
				return HttpResponse('')
			else:
				HttpResponseNotFound('')
	else:
		logout(request)
		messages.error(request, "Your account does not have sufficient privileges to perform this action. If you think this is an error, please contact your manager.")
		return redirect('/error/')


@login_required(login_url='/login/')
def del_onb(request):
	if request.method == 'POST':
		nh_uname = request.POST['col1']
		print(nh_uname)
		onboarding.objects.filter(newhire=nh_uname).delete()
		return HttpResponse('')


@login_required(login_url='/login')
def weeks(request):
	if request.user.profile.role=="MANAGER" or request.user.is_superuser:
		week = weeks_data.objects.all().order_by('weekid')
		user = User.objects.get(username=request.user)
		return render(request, 'weeks.html', {'week_data':week, 'user':user})
	else:
		try:
			onb = onboarding.objects.get(newhire=request.user.username)
			week = newhire_weeks.objects.filter(onboarding=onb).order_by('weekid')
			user = User.objects.get(username=request.user)
			return render(request, 'weeks.html', {'week_data':week, 'user':user})
		except:
			user = User.objects.get(username=request.user)
			return render(request, 'weeks.html', {'week_data':None, 'user':user})

@login_required(login_url='/login')
def add_week(request):
	if request.user.profile.role=="MANAGER" or request.user.is_superuser:
		if request.method == 'POST':
			week_id = request.POST['week_id']
			title = request.POST['title']
			if not weeks_data.objects.filter(weekid=week_id).exists():
				w = weeks_data(weekid = week_id, weektitle = title)
				w.save()
				return HttpResponse('')
			else:
				return HttpResponseNotFound('Week ID already exists!')
	else:
		logout(request)
		messages.error(request, "Your account does not have sufficient privileges to perform this action. If you think this is an error, please contact your manager.")
		return redirect('/error/')


@login_required(login_url='/login')
def del_week(request):
	if request.user.profile.role=="MANAGER" or request.user.is_superuser:
		if request.method == 'POST':
			week_id = request.POST['week_id']
			print(week_id)
			weeks_data.objects.filter(weekid=week_id).delete()
			return HttpResponse('')
	else:
		logout(request)
		messages.error(request, "Your account does not have sufficient privileges to perform this action. If you think this is an error, please contact your manager.")
		return redirect('/error/')


@login_required(login_url='/login/')
def week_content(request,  id):
	if request.user.profile.role=="MANAGER" or request.user.is_superuser:
		week = weeks_data.objects.get(weekid=id)
		c = content.objects.filter(weeks_data=week).order_by('task_id')
		return render(request, 'content.html', {'week_no':id, 'content':c})
	else:
		onb = onboarding.objects.get(newhire=request.user.username)
		week = newhire_weeks.objects.get(onboarding=onb, weekid=id)
		c = newhire_content.objects.filter(newhire_weeks=week).order_by('task_id')
		return render(request, 'content.html', {'week_no':id, 'content':c})

@login_required(login_url='/login')
def add_content(request):
	if request.user.profile.role=="MANAGER" or request.user.is_superuser:
		if request.method == 'POST':
			week_id = request.POST['week_id']
			task_id = request.POST['task_id']
			title = request.POST['title']
			week = weeks_data.objects.get(weekid=week_id)
			c = content(weeks_data=week, task_id=task_id, task=title)
			c.save()
			return HttpResponse('')
	else:
		logout(request)
		messages.error(request, "Your account does not have sufficient privileges to perform this action. If you think this is an error, please contact your manager.")
		return redirect('/error/')


@login_required(login_url='/login')
def del_content(request):
	if request.user.profile.role=="MANAGER" or request.user.is_superuser:
		if request.method == 'POST':
			week_id = request.POST['week_id']
			task = request.POST['task']
			week = weeks_data.objects.get(weekid=week_id)
			content.objects.get(weeks_data=week,task=task).delete()
			return HttpResponse('')
	else:
		logout(request)
		messages.error(request, "Your account does not have sufficient privileges to perform this action. If you think this is an error, please contact your manager.")
		return redirect('/error/')


def show_targets(request):
	if request.user.profile.role=="MANAGER" or request.user.is_superuser:
		target = targets.objects.all()
		return render(request, 'targets.html', {'target':target})		
	else:
		try:
			onb = onboarding.objects.get(newhire=request.user.username)
			nh_targets=newhire_targets.objects.filter(onboarding=onb)
			return render(request, 'targets.html', {'target':nh_targets})		
		except:
			return render(request, 'targets.html', {'target':None})

def add_target(request):
	if request.user.profile.role=="MANAGER" or request.user.is_superuser:
		if request.method == 'POST':
			target_id = request.POST['target_id']
			title = request.POST['title']
			target = targets.objects.filter(target=title)
			if not target:
				targets.objects.create(target_id = target_id, target=title)
				return HttpResponse('')
			else:
				return HttpResponseNotFound('')
	else:
		logout(request)
		messages.error(request, "Your account does not have sufficient privileges to perform this action. If you think this is an error, please contact your manager.")
		return redirect('/error/')


def del_target(request):
	if request.user.profile.role=="MANAGER" or request.user.is_superuser:
		if request.method == 'POST':
			title = request.POST['title']
			targets.objects.get(target=title).delete()
			return HttpResponse('')
	else:
		logout(request)
		messages.error(request, "Your account does not have sufficient privileges to perform this action. If you think this is an error, please contact your manager.")
		return redirect('/error/')

	