# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .forms import UserRegistrationForm, TimezoneForm, MeetingForm, MembersForm
from django.shortcuts import render, render_to_response
from django.contrib.auth import authenticate, login
from .models import Time_zone, Meeting, Members
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mail
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django import forms
import pytz
import datetime
import hashlib

# Create your views here.
def home(request):
    return render(request, 'login/home.html')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            userObj = form.cleaned_data
            username = userObj['username']
            email =  userObj['email']
            password =  userObj['password']
            if not (User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists()):
                User.objects.create_user(username, email, password)
                user = authenticate(username = username, password = password)
                login(request, user)
                return HttpResponseRedirect('/')
            else:
            	return render(request, 'login/register.html', {'form' : form})
    else:
        form = UserRegistrationForm()
    return render(request, 'login/register.html', {'form' : form})

def timezone(request):
	if request.method == 'POST':
		form = TimezoneForm(request.POST)
		if form.is_valid():
			userObj = form.cleaned_data
			current_user = request.user
			username = current_user.username
			zone =  userObj['timezone']
			if (User.objects.filter(username=username).exists()):
				if (Time_zone.objects.filter(username=username).exists()):
					temp = Time_zone()
					temp.update_timezone(username, zone)
				else:
					temp = Time_zone()
					temp.set_timezone(username, zone)
				return HttpResponseRedirect('/')
		else:
			return render(request, 'timezone.html', {'form' : form})
	else:
		form = TimezoneForm()
		return render(request, 'timezone.html', {'form' : form})
	return render(request, 'login/home.html', {'form' : form})

def meeting(request):
	if request.method == 'POST':
		form = MeetingForm(request.POST)
		if form.is_valid():
			userObj = form.cleaned_data
			current_user = request.user
			username = current_user.username
			title = userObj['title']
			st_date = userObj['st_date']
			end_date = userObj['end_date']
			if (User.objects.filter(username=username).exists()):
				temp = Meeting()
				user = User.objects.get(username=username)
				time = Time_zone.objects.get(username=username)
				hash_object = hashlib.md5(title+str(st_date)+str(end_date))
				hm = hash_object.hexdigest()
				temp.add_meeting(title, username, hm, st_date, end_date)
				request.session['hm'] = hm
				request.session['title'] = title
				request.session['st_date'] = st_date.strftime('%Y-%m-%d %H:%M:%S')
				request.session['end_date'] = end_date.strftime('%Y-%m-%d %H:%M:%S')
				request.session['timezone'] = time.timezone
				return render(request, 'add_members.html', {'hm':hm})
		else:
			return render(request, 'meeting.html', {'form' : form})
	else:
		form = MeetingForm()
		return render(request, 'meeting.html', {'form' : form})
	return render(request, 'login/home.html', {'form' : form})

def members(request):
	if request.method == 'POST':
		form = MembersForm(request.POST)
		if form.is_valid():
			userObj = form.cleaned_data
			current_user = request.user
			username = current_user.username
			from_email = current_user.email
			hash_meet = request.session.get('hm')
			title = request.session.get('title')
			dt1 = request.session.get('st_date')
			dt2 = request.session.get('end_date')
			tz = request.session.get('timezone')
			email = userObj['email']
			timezone = userObj['timezone']
			if (User.objects.filter(username=username).exists()):
				
				if not (Members.objects.filter(hash_meet=hash_meet, email=email).exists()):

					temp = Members()
					temp.add_status(hash_meet, title, email, timezone)

					tz1 = pytz.timezone(str(tz))
					tz2 = pytz.timezone(timezone)
					dt = datetime.datetime.strptime(dt1,"%Y-%m-%d %H:%M:%S")
					dt = tz1.localize(dt)
					dt = dt.astimezone(tz2)
					dt = dt.strftime("%Y-%m-%dT%H:%M:%S")
					nst = dt

					dt = datetime.datetime.strptime(dt2,"%Y-%m-%d %H:%M:%S")
					dt = tz1.localize(dt)
					dt = dt.astimezone(tz2)
					dt = dt.strftime("%Y-%m-%d %H:%M:%S")
					nend = dt
					
					subject = "Meeting Invite!"
					# message = "<HTML><BODY><h1> You have been invited to this meeting!</h1><a href=\"https://www.example.com?hm="+hash_meet+"&email="+email"&status=1\" >Yes</a><a href=\"https://www.example.com?hm="+hash_meet+"&email="+email"&status=2\" >Yes</a><a href=\"https://www.example.com?hm="+hash_meet+"&email="+email"&status=3\" >Yes</a></BODY></HTML>"
					text_content = 'Text'
					html_content = render_to_string(
					'email.html',
					{'hm': hash_meet, 'email': email}
					)
					text_content = strip_tags(html_content)
					msg = EmailMultiAlternatives(subject, text_content, from_email, [email])
					msg.attach_alternative(html_content, "text/html")
					msg.send()

					# msg = EmailMessage(subject, message, sender, email)
					# msg.content_subtype = "html"
					# msg.send()
					return render(request, 'add_members.html')
				else:
					return render(request, 'members.html', {'form' : form})		
		else:
			return render(request, 'members.html', {'form' : form})
	else:
		form = MembersForm()
		return render(request, 'members.html', {'form' : form})

def add_members(request):
	hm =  request.session.get('hm')
	return render_to_response('add_members.html', {'hm':hm})
	
def feedback(request, hm, email, status):
	# hm = request.GET.get('hm')
	temp = Members()
	temp.set_status(hm, int(status, email))
	return render_to_response('feedback.html', {'hm':hm})
