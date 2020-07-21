from BeginningDash.forms import LoginForm
from BeginningDash.forms import RegisterForm
from BeginningDash.models import say_something_nice
from BeginningDash.models import NewsByAdmin
from BeginningDash.models import MemberUpload
from BeginningDash.models import UMCU
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.db.models import Count
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.shortcuts import render,redirect
from BeginningDash.forms import (
    EditProfileForm, 
    UserEditForm
)
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render_to_response
from django.contrib.auth import (
     authenticate,
     login,
     logout
)
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib import auth
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from django.urls import reverse
from django.template import RequestContext
from django.db.models import Q


def status(request):
	status = "ONLINE"
	return {"user_status":status} 

def newscount(request):
	count = NewsByAdmin.objects.all().count()
	return {"news_count":count}

def user(request):
	user = ""
	user = request.user
	return {"user":user}

def statistics(request):
	if not request.user.is_authenticated():
		current_member = request.user
		return {"current_member":current_member}
	else:
		current_member = request.user
		item = MemberUpload.objects.filter(member=current_member)
		total_vids = MemberUpload.objects.filter(member=current_member).values('VIDEO').exclude(VIDEO = '',).count()
		total_auds = MemberUpload.objects.filter(member=current_member).values('AUDIO').exclude(AUDIO = '',).count()
		total_imgs = MemberUpload.objects.filter(member=current_member).values('IMAGE').exclude(IMAGE = '',).count()
		total_pdfs = MemberUpload.objects.filter(member=current_member).values('PDF').exclude(PDF = '',).count()
		total_total = total_vids + total_auds + total_imgs + total_pdfs
		# create a new manager ...
		total_files = MemberUpload.objects.filter(member=current_member).all().count()
		return {"total_files":total_files, 
		        "item":item,
		        "total_vids":total_vids,
		        "total_imgs":total_imgs,
		        "total_pdfs":total_pdfs,
		        "total_auds":total_auds,
		        "total_total":total_total,
		        }
def statistics_4_code(request):
	if not request.user.is_authenticated():
		current_member = request.user
		return {"current_member":current_member}
	else:
		current_member = request.user
		item_4_code = UMCU.objects.filter(user=current_member)
		total_html = UMCU.objects.filter(user=current_member).values('HTML').exclude(HTML = '',).count()
		total_css = UMCU.objects.filter(user=current_member).values('CSS').exclude(CSS = '',).count()
		total_total_4_code = total_html + total_css 
		# create a new manager ...
		total_files_4_code = UMCU.objects.filter(user=current_member).all().count()
		return {"total_files_4_code":total_files_4_code, 
		        "item_4_code":item_4_code,
		        "total_html":total_html,
		        "total_css":total_css,
		        "total_total_4_code":total_total_4_code,
		        }


def say_sth(request):
	peoples_view = say_something_nice.published.filter(status= 'show')[:4]
	return  {	
			'peoples_view': peoples_view,
			}













