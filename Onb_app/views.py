from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
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
	if user.profile.firstlogin:
		user.profile.firstlogin = False
		user.save()
		return render(request, 'welcome.html', {'title': 'Welcome', 'user':user})
	else:
		return HttpResponseRedirect('/home/')

	
@login_required(login_url='/login/')
def home(request):
	prof = User.objects.get(username=request.user.username)
	return render(request, 'home.html', {'title': 'Onboarding Home', 'prof':prof})


@login_required(login_url='/login/')
def viewsupportengineers(request):
	if request.user.profile.role=="MANAGER" or request.user.is_superuser:
		eng = Profile.objects.filter(role='ENGINEER')
		manager = Profile.objects.filter(role='MANAGER')
		nh = Profile.objects.filter(role='NEW_HIRE')
		return render(request, 'userpage.html', {'eng': eng, 'manager':manager, 'nh':nh})
	else:
		logout(request)
		messages.error(request, "Your account does not have sufficient privileges to perform this action. If you think this is an error, please contact your manager.")
		return redirect('/error/')

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

@login_required(login_url='/login')
def weeks(request):
	week = weeks_data.objects.all()
	user = User.objects.get(username=request.user)
	return render(request, 'weeks.html', {'week':week, 'user':user})