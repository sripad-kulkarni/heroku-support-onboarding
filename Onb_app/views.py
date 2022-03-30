import re
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotFound, JsonResponse
import json as simplejson
from .forms import UserRegisterForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from .models import *
from django.contrib.auth.models import User
import datetime
from django.db.models import Q
from django.core import serializers
from django.db.models import Value
from django.db.models.functions import Concat
from django.db.models import Count, Sum
import requests
import os
from django.utils import timezone
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
		        audit_logger.objects.create(user=request.user.username, action='CREATE_USER: `' + user.username + '`')
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
	audit_logger.objects.create(user=request.user.username, action='LOGOUT')
	logout(request)
	return redirect('/login/')


def error(request):
	return render(request, 'error.html')


@login_required(login_url='/login/')
def welcome(request):
	user = User.objects.get(username=request.user.username)
	if user.profile.firstlogin:
		user.profile.firstlogin = False
		user.save()
		audit_logger.objects.create(user=request.user.username, action='FIRST LOGIN')
		if user.profile.role == 'NEW_HIRE':
			return render(request, 'welcome.html', {'title': 'Welcome', 'user':user})
		else:
			return render(request, 'welcome_default.html', {'title':'welcome', 'user':user})
	else:
		audit_logger.objects.create(user=request.user.username, action='LOGIN')
		return HttpResponseRedirect('/home/')



@login_required(login_url='/login/')
def profile_page(request):
	prof = User.objects.get(username=request.user.username)
	'''
	requests.post(os.environ.get("TILL_URL"), json={
	    "phone": [prof.profile.phone],
	    "text" : "Hello Heroku!"
	})'''
	return render(request, 'profile_page.html', {'prof':prof})


@login_required(login_url='/login')
def updateprofile(request):
	if request.method == 'POST':
		firstname = request.POST['firstname']
		lastname = request.POST['lastname']
		email = request.POST['email']
		phone = request.POST['phone']
		user = User.objects.get(username=request.user.username)
		user.profile.firstname = firstname
		user.profile.lastname = lastname
		user.profile.email = email
		user.profile.phone = phone
		user.save()
		audit_logger.objects.create(user=request.user.username, action='UPDATE_PROFILE')
		return HttpResponse('')

	
@login_required(login_url='/login/')
def home(request):
	if request.user.profile.role=="MANAGER" or request.user.is_superuser:
		onb = onboarding.objects.all()
		usr = User.objects.all()
		target = targets.objects.all()
		return render(request, 'manager_home.html', {'onb':onb, 'usr':usr, 'target': targets, 'title': "Onboarding - Home"})
	elif request.user.profile.role=="ENGINEER":
		onb = onboarding.objects.filter(Q(onboardingbuddy=request.user.username) | Q(trailguide=request.user.username))
		usr = User.objects.all()
		target = targets.objects.all()
		return render(request, 'manager_home.html', {'onb':onb, 'usr':usr, 'target': targets, 'title': "Onboarding - Home"})
	else:
		prof = User.objects.get(username=request.user.username)
		try:
			onb = onboarding.objects.get(newhire=request.user.username)
			nh_week = newhire_weeks.objects.filter(onboarding__newhire=request.user.username).order_by('weekid')
			completed = 0
			count = 0
			for nhw in nh_week:
				completed = completed + newhire_content.objects.filter(newhire_weeks=nhw,status='True').count()
				count = count + newhire_content.objects.filter(newhire_weeks=nhw).count()
			if nh_week.count() > 0:
				perc = round((completed/count)*100, 2)
			else:
				perc = 0.0
			onb.progress = perc
			nh_targets = newhire_targets.objects.filter(onboarding__newhire=request.user.username)
			target_achieved = newhire_targets.objects.filter(onboarding__newhire=request.user.username, status=True).count()
			if nh_targets.count() > 0:
				nh_t_progress = (target_achieved/nh_targets.count()) * 100
			else:
				nh_t_progress = 0
			usr = User.objects.all()
			approved_items = Q(newhire_access_item__status='Approved')
			requested_items = Q(newhire_access_item__status='Requested')
			tabs = newhire_access_section.objects.filter(onboarding__newhire=request.user.username).annotate(item_count=Count('newhire_access_item')).annotate(approved=Count('newhire_access_item', approved_items)).annotate(requested=Count('newhire_access_item__status',requested_items))
			approved = sum(tabs.values_list('approved', flat=True))
			requested = sum(tabs.values_list('requested', flat=True))
			total = sum(tabs.values_list('item_count' ,flat=True))
			items = newhire_access_item.objects.filter(newhire_access_section__onboarding__newhire=request.user.username).order_by('name')
			nh_resources = resources.objects.filter(onboarding__newhire=request.user.username)
			return render(request, 'home.html', {'title': 'Onboarding - Home', 'prof':prof, 'onb':onb, 'usr':usr, 'nh_week':nh_week, 'nh_targets':nh_targets, 'nh_t_progress':nh_t_progress, 'tabs':tabs,'items':items ,'requested':requested, 'approved':approved, 'total':total, 'resources':nh_resources})
		except Exception as ex:
			onb = None
			return render(request, 'home.html', {'title': 'Onboarding - Home', 'prof':prof, 'onb':onb, 'nh_targets':None})

@login_required(login_url='/login/')
def audit(request):
	if request.user.profile.role=="MANAGER" or request.user.is_superuser:
		try:
			from_date = request.POST['from']
			to_date = request.POST['to']
			search = request.POST['search']
			if from_date == '' and to_date == '':
				if not search == '':
					audit = reversed(audit_logger.objects.filter(Q(user__contains=search) | Q(action__contains=search)))
				else:
					audit = reversed(audit_logger.objects.all())
			else:
				if not search == '':
					audit = reversed(audit_logger.objects.filter(Q(user__contains=search) | Q(action__contains=search), timestamp__range=[from_date,to_date]))
				else:
					audit = reversed(audit_logger.objects.filter(timestamp__range=[from_date,to_date]))
			return render(request, 'results.html', { 'audit':audit, 'title':'Audit Log' })
		except:
			audit = reversed(audit_logger.objects.all())
			return render(request, 'audit.html', { 'audit':audit, 'title':'Audit Log' })
	else:
		logout(request)
		messages.error(request, "Your account does not have sufficient privileges to perform this action. If you think this is an error, please contact your manager.")
		return redirect('/error/')


@login_required(login_url='/login/')
def viewsupportengineers(request):
	if request.user.profile.role=="MANAGER" or request.user.is_superuser:
		eng = Profile.objects.filter(role='ENGINEER').order_by('firstname')
		manager = Profile.objects.filter(role='MANAGER').order_by('firstname')
		nh = Profile.objects.filter(role='NEW_HIRE').order_by('firstname')
		onb = onboarding.objects.all()
		usr = User.objects.all()
		return render(request, 'userpage.html', {'eng': eng, 'manager':manager, 'nh':nh, 'onb':onb, 'usr':usr, 'title': "Engineers"})
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
				access = access_section.objects.all()
				for a in access:
					acc = newhire_access_section.objects.create(onboarding=onb, s_id=a.s_id, name=a.name)
					item = access_item.objects.filter(access_section=a)
					for i in item:
						newhire_access_item.objects.create(newhire_access_section=acc, item_id=i.item_id, name=i.name)
				audit_logger.objects.create(user=request.user.username, action='**ASSIGN NEW HIRE** `'+new_hire+'` to TRAIL GUIDE `'+trail_guide+'`, ONBOARDING BUDDY `'+onb_buddy+'`, MANAGER `'+the_manager+'`')
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
		onboarding.objects.filter(newhire=nh_uname).delete()
		audit_logger.objects.create(user=request.user.username, action='**REMOVE ASSIGNMENT NEW HIRE** `'+nh_uname+'`')
		return HttpResponse('')


@login_required(login_url='/login')
def weeks(request):
	if request.user.profile.role=="MANAGER" or request.user.is_superuser or request.user.profile.role=="ENGINEER":
		week = weeks_data.objects.all().order_by('weekid')
		user = User.objects.get(username=request.user)
		return render(request, 'weeks.html', {'week_data':week, 'user':user, 'title': "Onboarding Plan - Weeks"})
	else:
		try:
			onb = onboarding.objects.get(newhire=request.user.username)
			week = newhire_weeks.objects.filter(onboarding=onb).order_by('weekid')
			user = User.objects.get(username=request.user)
			content = newhire_content.objects.filter(newhire_weeks__onboarding=onb)
			return render(request, 'weeks.html', {'week_data':week, 'user':user, content:'content', 'title': "Onboarding Plan - Weeks"})
		except:
			user = User.objects.get(username=request.user)
			return render(request, 'weeks.html', {'week_data':None, 'user':user, 'title': "Onboarding Plan - Weeks"})

@login_required(login_url='/login')
def add_week(request):
	if request.user.profile.role=="MANAGER" or request.user.is_superuser:
		if request.method == 'POST':
			week_id = request.POST['week_id']
			title = request.POST['title']
			if not weeks_data.objects.filter(weekid=week_id).exists():
				w = weeks_data(weekid = week_id, weektitle = title)
				w.save()
				audit_logger.objects.create(user=request.user.username, action='**ADD WEEEK:** `'+week_id+'` - `'+title+'`')
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
			weeks_data.objects.filter(weekid=week_id).delete()
			audit_logger.objects.create(user=request.user.username, action='**REMOVE WEEEK:** `'+week_id+'`')
			return HttpResponse('')
	else:
		logout(request)
		messages.error(request, "Your account does not have sufficient privileges to perform this action. If you think this is an error, please contact your manager.")
		return redirect('/error/')


@login_required(login_url='/login/')
def week_content(request,  id):
	if request.user.profile.role=="MANAGER" or request.user.is_superuser or request.user.profile.role=="ENGINEER":
		week = weeks_data.objects.get(weekid=id)
		c = content.objects.filter(weeks_data=week).order_by('task_id')
		return render(request, 'content.html', {'week_no':id, 'week':week, 'content':c, 'title': "The Week"})
	else:
		onb = onboarding.objects.get(newhire=request.user.username)
		week = newhire_weeks.objects.get(onboarding=onb, weekid=id)
		c = newhire_content.objects.filter(newhire_weeks=week).order_by('task_id')
		return render(request, 'content.html', {'week_no':id, 'week':week, 'content':c, 'week':week, 'title':"The Week"})

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
			audit_logger.objects.create(user=request.user.username, action='**ADD CONTENT:** Week `'+week_id+'` - Task `'+task_id+'` - `'+title+'`')
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
			content.objects.get(weeks_data=week,task_id=task).delete()
			audit_logger.objects.create(user=request.user.username, action='**REMOVE CONTENT:** Week `'+week_id+'` - Task `'+task+'`')
			return HttpResponse('')
	else:
		logout(request)
		messages.error(request, "Your account does not have sufficient privileges to perform this action. If you think this is an error, please contact your manager.")
		return redirect('/error/')


def show_targets(request):
	if request.user.profile.role=="MANAGER" or request.user.is_superuser or request.user.profile.role=="ENGINEER":
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

def target_check(request):
	target_name = request.POST['target_name']
	target_check = request.POST['target_check']
	target = newhire_targets.objects.get(onboarding__newhire=request.user.username, target=target_name)
	if target_check == 'true':
		target.status=True
	else: 
		target.status=False
	target.save()
	return HttpResponse('')


def content_check(request):
	content_name = request.POST['content_name']
	content_check = request.POST['content_check']
	week_no = request.POST['week_no']
	content = newhire_content.objects.get(newhire_weeks__onboarding__newhire=request.user.username, newhire_weeks__weekid = week_no, task_id = content_name)
	if content_check == 'true':
		content.status = True
	else:
		content.status = False
	content.save()
	audit_logger.objects.create(user=request.user.username, action='**WEEK TASK CHECKED:** WEEK - `'+week_no+'`, TASK - `'+content_name+'`')
	nh_week_progress = newhire_content.objects.filter(newhire_weeks__onboarding__newhire=request.user.username, newhire_weeks__weekid = week_no, status=True).count()
	nh_content = newhire_content.objects.filter(newhire_weeks__onboarding__newhire=request.user.username, newhire_weeks__weekid = week_no).count()
	nh_week_perc = round((nh_week_progress/nh_content)*100, 2)
	nh_week = newhire_weeks.objects.get(onboarding__newhire=request.user.username, weekid=week_no)
	nh_week.status = nh_week_perc
	nh_week.save()
	return HttpResponse('')

def check_form(request):
	if request.method == 'POST':
		name=request.POST['name']
		prof = User.objects.get(username=name)
		onb = onboarding.objects.get(newhire=name)
		usr = User.objects.all()
		nh_week = newhire_weeks.objects.filter(onboarding__newhire=name)
		completed = 0
		count = 0
		for nhw in nh_week:
			completed = completed + newhire_content.objects.filter(newhire_weeks=nhw, status=True).count()
			count = count + newhire_content.objects.filter(newhire_weeks=nhw).count()
		'''
		completed = newhire_weeks.objects.filter(onboarding__newhire=name, status='100.0').count()
		'''
		if nh_week.count() > 0:
			perc = round((completed/count)*100, 2)
		else:
			perc = 0.0
		''' weeks done '''
		''' Targets below '''
		onb.progress = perc
		nh_targets = newhire_targets.objects.filter(onboarding__newhire=name)
		target_achieved = newhire_targets.objects.filter(onboarding__newhire=name, status=True).count()
		if nh_targets.count() > 0:
			nh_t_progress = (target_achieved/nh_targets.count()) * 100
		else:
			nh_t_progress = 0
		''' Targets Done'''
	return render(request, 'check_form.html', {'title': 'Onboarding Home', 'prof':prof, 'onb':onb, 'usr':usr, 'nh_week':nh_week, 'nh_targets':nh_targets, 'nh_t_progress':nh_t_progress})

def view_details(request):
	if request.method=='POST':
		full_name = request.POST['name']
		p = Profile.objects.annotate(fullname=Concat('firstname', Value(' '), 'lastname')).get(fullname=full_name)
		name = p.user.username
		prof = User.objects.get(username=name)
		onb = onboarding.objects.get(newhire=name)
		usr = User.objects.all()
		nh_week = newhire_weeks.objects.filter(onboarding__newhire=name).order_by('weekid')
		print(nh_week.values())
		completed = 0
		count = 0
		for nhw in nh_week:
			completed = completed + newhire_content.objects.filter(newhire_weeks=nhw, status=True).count()
			count = count + newhire_content.objects.filter(newhire_weeks=nhw).count()
		'''
		completed = newhire_weeks.objects.filter(onboarding__newhire=name, status='100.0').count()
		'''
		if nh_week.count() > 0:
			perc = round((completed/count)*100, 2)
		else:
			perc = 0.0
		''' weeks done '''
		''' Targets below '''
		onb.progress = perc
		nh_targets = newhire_targets.objects.filter(onboarding__newhire=name)
		target_achieved = newhire_targets.objects.filter(onboarding__newhire=name, status=True).count()
		if nh_targets.count() > 0:
			nh_t_progress = (target_achieved/nh_targets.count()) * 100
		else:
			nh_t_progress = 0
		''' Targets Done'''
		'''Access Req below'''
		approved_items = Q(newhire_access_item__status='Approved')
		requested_items = Q(newhire_access_item__status='Requested')
		tabs = newhire_access_section.objects.filter(onboarding__newhire=name).annotate(item_count=Count('newhire_access_item')).annotate(approved=Count('newhire_access_item', approved_items)).annotate(requested=Count('newhire_access_item__status',requested_items))
		approved = sum(tabs.values_list('approved', flat=True))
		requested = sum(tabs.values_list('requested', flat=True))
		total = sum(tabs.values_list('item_count' ,flat=True))
		items = newhire_access_item.objects.filter(newhire_access_section__onboarding__newhire=name).order_by('name')
		nh_resources = resources.objects.filter(onboarding__newhire=name)
		return render(request, 'check_form.html', {'title': 'Onboarding Home', 'prof':prof, 'onb':onb, 'usr':usr, 'nh_week':nh_week, 'nh_targets':nh_targets, 'nh_t_progress':nh_t_progress, 'tabs':tabs,'items':items ,'requested':requested, 'approved':approved, 'total':total, 'resources':nh_resources})

'''
def check_accesses(request):
	if request.method=='POST':
		name = request.POST['name']
		try:
			onb = onboarding.objects.get(newhire=name)
			access = newhire_access_section.objects.filter(onboarding=onb).order_by('s_id')
			items = newhire_access_item.objects.filter(newhire_access_section=access).order_by('item_id')
			return render(request, 'eng_access_req.html', {'tabs':access, 'items':items})
		except:
			return render(request, 'eng_access_req.html', {'tabs':None, 'items':None})			
'''

def check_weeks(request):
	if request.method == 'POST':
		name=request.POST['name']
		try:
			onb = onboarding.objects.get(newhire=name)
			week = newhire_weeks.objects.filter(onboarding=onb).order_by('weekid')
			user = User.objects.get(username=request.user)
			return render(request, 'eng_week_check.html', {'week_data':week, 'user':user})
		except:
			user = User.objects.get(username=name)
			return render(request, 'eng_week_check.html', {'week_data':None, 'user':user})

def check_targets(request):
	if request.method == 'POST':
		name=request.POST['name']
		try:
			onb = onboarding.objects.get(newhire=name)
			nh_targets=newhire_targets.objects.filter(onboarding=onb)
			return render(request, 'eng_targets_check.html', {'target':nh_targets})		
		except:
			return render(request, 'eng_targets_check.html', {'target':None})

def check_content(request):
	if request.method == 'POST':
		full_name=request.POST['name']
		id = request.POST['week_id']
		p = Profile.objects.annotate(fullname=Concat('firstname', Value(' '), 'lastname')).get(fullname=full_name)
		name = p.user.username
		prof = User.objects.get(username=name)
		onb = onboarding.objects.get(newhire=name)
		week = newhire_weeks.objects.get(onboarding=onb, weekid=id)
		c = newhire_content.objects.filter(newhire_weeks=week).order_by('task_id')
		return render(request, 'eng_content_check.html', {'week_no':id, 'content':c, 'week':week})


def access_req(request):
	if request.user.profile.role=="MANAGER" or request.user.is_superuser:
		tabs = access_section.objects.all()
		items = access_item.objects.all().order_by('name')
		return render(request, 'access_req.html', {'tabs': tabs, 'items': items, 'requested':0, 'approved':0, 'total':0, 'title': "Access Requests"})
	else:
		approved_items = Q(newhire_access_item__status='Approved')
		requested_items = Q(newhire_access_item__status='Requested')
		tabs = newhire_access_section.objects.filter(onboarding__newhire=request.user.username).annotate(item_count=Count('newhire_access_item')).annotate(approved=Count('newhire_access_item', approved_items)).annotate(requested=Count('newhire_access_item__status',requested_items))
		approved = sum(tabs.values_list('approved', flat=True))
		requested = sum(tabs.values_list('requested', flat=True))
		total = sum(tabs.values_list('item_count' ,flat=True))
		items = newhire_access_item.objects.filter(newhire_access_section__onboarding__newhire=request.user.username).order_by('name')
		return render(request, 'access_req.html', {'tabs': tabs, 'items': items, 'requested':requested, 'approved':approved, 'total':total, 'title': "Access Requests"})

def access_tab(request):
	if request.user.profile.role=="MANAGER" or request.user.is_superuser:
		if request.method == 'POST':
			tab_id = request.POST['tab_id']
			name= request.POST['name']
			access_section.objects.create(s_id=tab_id, name=name)
			audit_logger.objects.create(user=request.user.username, action='**ADD ACCESS SECTION:** `'+name+'`')
			return HttpResponse('')

def del_tab(request):
	if request.user.profile.role=="MANAGER" or request.user.is_superuser:
		if request.method == 'POST':
			name = request.POST['name']
			access_section.objects.get(name=name).delete()
			audit_logger.objects.create(user=request.user.username, action='**REMOVE ACCESS SECTION:** `'+name+'`')
			return HttpResponse('')

def add_item(request):
	if request.user.profile.role=="MANAGER" or request.user.is_superuser:
		if request.method == 'POST':
			section = request.POST['section']
			item_id = request.POST['item_id']
			name = request.POST['name']
			s = access_section.objects.get(name=section)
			access_item.objects.create(access_section=s, item_id=item_id, name=name) 
			audit_logger.objects.create(user=request.user.username, action='**ADD ACCESS ITEM:** SECTION - `'+section+'`, ITEM - `'+name+'`')
			return HttpResponse('')

def get_items(request):
	name = request.GET['name']
	section = access_section.objects.get(name=name)
	items = access_item.objects.filter(access_section=section)
	data = list(items.values())
	return JsonResponse(data, safe=False)


def del_item(request):
	if request.user.profile.role=="MANAGER" or request.user.is_superuser:
		if request.method == 'POST':
			section = request.POST['section']
			name = request.POST['name']
			s = access_section.objects.get(name=section)
			access_item.objects.get(access_section = s, name = name).delete()
			audit_logger.objects.create(user=request.user.username, action='**REMOVE ACCESS ITEM:** SECTION - `'+section+'`, ITEM - `'+name+'`')
			return HttpResponse('')

def access_req_update(request):
	if request.method == 'POST':
		name = request.POST['name']
		value = request.POST['value']
		item = newhire_access_item.objects.get(newhire_access_section__onboarding__newhire = request.user.username, name=name)
		item.status = value
		item.save()
		audit_logger.objects.create(user=request.user.username, action='**ACCESS REQ UPDATE:**  - `'+name+'` - `'+value+'`')
		return HttpResponse()

def add_resource(request):
	if request.method=='POST':
		if request.user.profile.role == 'MANAGER' or request.user.is_superuser or request.user.profile.role=='ENGINEER':
			full_name = request.POST['nh_name']
			p = Profile.objects.annotate(fullname=Concat('firstname', Value(' '), 'lastname')).get(fullname=full_name)
			nh_name = p.user.username
		else:
			nh_name = request.user.username
		name = request.POST['key']
		value = request.POST['value']
		print(value, value.startswith('http://'), value.startswith('https://'))
		if not value.startswith('http://') and not value.startswith('https://'):
			value = "http://" + value
			print(value)
		onb = onboarding.objects.get(newhire=nh_name)
		temp = resources.objects.filter(onboarding = onb, title=name).exists()
		if temp:
			res = resources.objects.get(onboarding = onb, title=name)
			res.value = value
			res.save()
		else:
			res = resources(onboarding = onb, title=name, value=value)
			res.save()
		audit_logger.objects.create(user=request.user.username, action='**ADD RESOURCE:** - `'+name+'` - `'+value+'`')
		return HttpResponse('')

def del_resource(request):
	if request.method == 'POST':
		name = request.POST['key']
		if request.user.profile.role == 'MANAGER' or request.user.is_superuser or request.user.profile.role=='ENGINEER':
			full_name = request.POST['nh_name']
			p = Profile.objects.annotate(fullname=Concat('firstname', Value(' '), 'lastname')).get(fullname=full_name)
			nh_name = p.user.username
		else:
			nh_name = request.user.username
		resources.objects.get(onboarding__newhire=nh_name, title=name).delete()
		audit_logger.objects.create(user=request.user.username, action='**REMOVE RESOURCE:** - `'+name+'`')
		return HttpResponse('')

@login_required
def change_password(request):
	if request.user.is_authenticated:
		if request.method == 'POST':
			form = PasswordChangeForm(user = request.user, data = request.POST)
			if form.is_valid():
				form.save()
				update_session_auth_hash(request, form.user)
				messages.success(request, "Your password has been changed successfully!")
				return redirect('/profile/change_password/')
		else:
			form = PasswordChangeForm(request.POST)
		return render(request, 'change_pass.html', {'form':form})
	else:
		messages.error(request, "Please login to perform this action!")
		return redirect('/login/')
