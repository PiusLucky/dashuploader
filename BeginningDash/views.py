from django.shortcuts import render,redirect
from BeginningDash.forms import (
	LoginForm,
	RegisterForm,
	EditProfileForm, 
	UserEditForm
	)
from .forms import contactForm
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render_to_response
from django.contrib.auth import (
     authenticate,
     login,
     logout,
    )
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import *
from BeginningDash.models import *
from BeginningDash.forms import *
from django.contrib.auth.models import User
from django.contrib import auth
from django.core.exceptions import ObjectDoesNotExist
from BeginningDash.models import MemberUploadForm
from BeginningDash.models import MemberUploadForm
from django.shortcuts import redirect
from django.urls import reverse
from django.template import RequestContext
from django.db.models import Q
import datetime
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.views.generic import View
import datetime
from django.template.loader import get_template
from BeginningDash.utils import render_to_pdf 
from templated_email import send_templated_mail
from django.core.mail import EmailMessage
from django.template import Context, Template
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.forms import PasswordChangeForm		


def homepage(request):
	title = "Home"
	Empty_File = "No Files Uploaded Yet."
	current_member = request.user
	files = MemberUpload.objects.filter(member=current_member)
	if request.method == 'POST':
		fileupload_form = MemberUploadForm(request.POST or None, request.FILES or None)
		if fileupload_form.is_valid():
			new_file = MemberUpload (
				member=current_member, 
				VIDEO = request.FILES.get('VIDEO',None),
				AUDIO = request.FILES.get('AUDIO', None),  
				PDF = request.FILES.get('PDF', None),  
				IMAGE = request.FILES.get('IMAGE', None),
				# since this is a required field in my models
				# it's logical to not set it to None
				file_group = request.POST.get('file_group'), 
				date_uploaded = request.POST.get('date_uploaded'),
				comment = request.POST.get('comment'),
		  )
			new_file.save()
			return render(request, "Beginning/homepage.html", { 
				"title": title, 
				"fileupload_form":fileupload_form ,
				'files':files,
				'member': current_member,
				'Empty_File':Empty_File,
				'success_msg':'successfully Uploaded !!',							 
			})
		else:            
			return render(request, "Beginning/homepage.html", { 
				"title": title, 
				"fileupload_form":fileupload_form ,
				'files':files,
				'member': current_member,
				'Empty_File':Empty_File,
				'error_msg':'Upload failed, please correct error below, and try again!!',
     	})
	else:
 		fileupload_form = MemberUploadForm()
	return render(request, "Beginning/homepage.html", { 
		"title": title, 
		"fileupload_form":fileupload_form ,
		'files':files,
		'member': current_member,
		'Empty_File':Empty_File,
	})
def UCU(request):
	title = "Coding"
	Empty_File = "No Code Uploaded Yet."
	current_user = request.user
	code_files = UMCU.objects.filter(user=current_user)
	if request.method == 'POST':
		UMCU_form = UMCUForm(request.POST or None, request.FILES or None)
		if UMCU_form.is_valid():			 
			code_file = UMCU(      
				user=current_user, 
				# since this is a required field in my models
				# it's logical to not set it to None
				folder = request.POST.get('folder'),
				uploaded_time = request.POST.get('uploaded_time'),
				says = request.POST.get('says'),
				HTML = request.FILES.get('HTML', None),  
				CSS = request.FILES.get('CSS', None),  
			)
			code_file.save()
			return render(request, "Beginning/code.html", {
				"title": title, 
				"UMCU_form":UMCU_form ,
				'code_files':code_files,
				'member': current_user,
				'Empty_File':Empty_File,
				'mysuccessmessage':'Code Uploaded Successfully .'
			})
		else:            
			return render(request, "Beginning/code.html", { 
				"title": title, 
				"UMCU_form":UMCU_form ,
				'code_files':code_files,
				'member': current_user,
				'Empty_File':Empty_File,
				'myerrormessage':'Opps, Error encountered while trying to upload your Code, Check fields and try again!!'
     	} )
	else:
 		UMCU_form = UMCUForm()
	return render(request, "Beginning/code.html", {     
		"title": title, 
		"UMCU_form":UMCU_form ,
		'code_files':code_files,
		'member': current_user,
		'Empty_File':Empty_File,
  })


def created_document(request):
	return render(request, 'Beginning/created_document.html')


def view_profile(request, pk=None):
	free_status = "Free User"
	premium_status = "Premium User"
	peoples_view = say_something_nice.published.filter(status='show')[2:3]
	peoples_view1 = say_something_nice.published.filter(status='show')[:1]
	peoples_view2 = say_something_nice.published.filter(status='show')[1:2]
	Admin_news = NewsByAdmin.objects.all()[:3]
	Dashboard = "Dashboard"
	user = ""
	user = request.user
	if request.method == 'POST':
		say_something =  say_something_nice_Form(request.POST or None, request.FILES or None)
		if say_something.is_valid():
			say_something.save()
			say_something =  say_something_nice_Form()
			return render(request,"Beginning/profile.html", {
				'user': user,
				"title": Dashboard,	
				'peoples_view': peoples_view,
				"Admin_news":Admin_news,
				"free_status":free_status,
				"premium_status":premium_status,
				'say_somethingForm': say_something_nice_Form,
				'say_success':'Your Review has been submitted successfully.'
			}) 
		else:            
			return render(request,"Beginning/profile.html", {
				'user': user,
				"title": Dashboard,	
				'peoples_view': peoples_view,
				"Admin_news":Admin_news,
				"free_status":free_status,
				"premium_status":premium_status,
				'say_somethingForm': say_something_nice_Form,
				'say_error':'Opps, An error ocurred.Your Review could not be proccessed at this time.Try Again!!.'
			}) 
	else:
		say_something = say_something_nice_Form()
	return render(request, "Beginning/profile.html", { 
		'user': user,
		"title": Dashboard,
		'peoples_view': peoples_view,
		"Admin_news":Admin_news,
		"free_status":free_status,
		"premium_status":premium_status,
		'peoples_view1': peoples_view1,
		'peoples_view2': peoples_view2,
		'say_somethingForm': say_something_nice_Form,
	})


def edit_profile(request):
	title = "Edit profile"
	profile_form = ''
	user_form = ''
	user = request.user
	free_status = "Free User"
	premium_status = "Premium User"
	if request.method == 'POST':
		profile_form = EditProfileForm(data=request.POST, instance=request.user.userprofile, files=request.FILES)
		user_form = UserEditForm(data=request.POST, instance=request.user)
		if profile_form.is_valid() and user_form.is_valid():
			profile_form.save()
			user_form.save()
			return render(request, "Beginning/edit_profile.html", {
				'user': user,
				"title": title,
				"profile_form":profile_form,
				"user_form":user_form,
				"free_status":free_status,
				"premium_status":premium_status,
				'save_success':'Your Profile has been updated successfully.'
			})
		else:
			profile_form = EditProfileForm(instance=request.user.userprofile, files=request.FILES)
			user_form = UserEditForm(instance=request.user)
			return render(request, "Beginning/edit_profile.html", {
				'user': user,
				"title": title,
				"profile_form":profile_form,
				"user_form":user_form,
				"free_status":free_status,
				"premium_status":premium_status,
				'save_error':'Opps, An error ocurred. Check in fields and try Again!!'
			})

	else:
	    profile_form = EditProfileForm(instance=request.user.userprofile, files=request.FILES)
	    user_form = UserEditForm(instance=request.user)
	args = {
		'profile_form': profile_form, 
		'user_form': user_form,
		"free_status":free_status,
		"premium_status":premium_status,
		"title":title,
  }
	return render(request, 'Beginning/edit_profile.html', args)


def loginX_regX(request):
	title = "login-register"
	login_form = LoginForm(request.POST or None)
	form1 = RegisterForm(request.POST)
	if request.method == 'GET':
		# This call () clears the form
		login_form = LoginForm()
		form1 = RegisterForm()
	if request.method == "POST":
		if request.POST.get('mylogin') == 'log-in':
			if login_form.is_valid():
				username = login_form.cleaned_data.get("username")
				password = login_form.cleaned_data.get('password')
				user = authenticate(username=username, password=password)
				login(request, user)
				return redirect('/home/dashboard')
			else:
				# If the form is not valid ,the command clears the register form 
				# and leave validation error message present in login form...
				form1 = RegisterForm()
				return render(request, "base.html", {        
					"title": title, 
					"form":login_form ,	
					"frm":form1 ,	
					'loginerrormessage':'Opps, Error encountered while trying to get you authenticated, Please try again!!'
				})
		elif request.POST.get('submit-reg') == 'sign-up':	
			if form1.is_valid():
				now = datetime.datetime.now()
				username = form1.cleaned_data["username"]
				first_name = form1.cleaned_data["first_name"]
				last_name = form1.cleaned_data["last_name"]
				email = form1.cleaned_data["email"]
				password = form1.cleaned_data["password"]
				confirm_password = form1.cleaned_data["confirm_password"]
				User.objects.create_user(username = username ,first_name=first_name,last_name=last_name,email=email,password=password)
				messages.success(request, 'Your account with username |%s| has been created successfully today at  %s !!!.' % (username, now) )
				return redirect('/register/response')
			else:
				# If the form is not valid ,the command clears the login form 
				# and leave validation error message present in register form...
				login_form = LoginForm()
				return render(request, "base.html", {       
					"title": title, 
					"form":login_form ,	
					"frm":form1 ,	
					'signuperrormessage':'Opps, Error encountered while trying to sign you up, Please try again!!'
				})
	return render(request, "base.html",{"form":login_form, 'frm':form1, "title": title,})


def register_response(request):
	title = "register|response"
	return render(request, 'newpartials/regsuccess.html', { "title":title })


def logout(request):
	title = "log-out"
	auth.logout(request) 
	login_form = LoginForm(request.POST or None)
	form1 = RegisterForm(request.POST)
	if request.method == 'GET':
		login_form = LoginForm()
		form1 = RegisterForm()
	if request.method == "POST":
		if request.POST.get('mylogin') == 'log-in':
			if login_form.is_valid():
				username = login_form.cleaned_data.get("username")
				password = login_form.cleaned_data.get('password')
				user = authenticate(username=username, password=password)
				login(request, user)
				return redirect('/home/dashboard')
			else:
				form1 = RegisterForm()
				return render(request, "base.html", {        
					"title": title, 
					"form":login_form ,	
					"frm":form1 ,	
					'loginerrormessage':'Opps, Error encountered while trying to get you authenticated, Please try again!!'
				})
		elif request.POST.get('submit-reg') == 'sign-up':	
			if form1.is_valid():
				now = datetime.datetime.now()
				username = form1.cleaned_data["username"]
				first_name = form1.cleaned_data["first_name"]
				last_name = form1.cleaned_data["last_name"]
				email = form1.cleaned_data["email"]
				password = form1.cleaned_data["password"]
				confirm_password = form1.cleaned_data["confirm_password"]
				User.objects.create_user(username = username ,first_name=first_name,last_name=last_name,email=email,password=password)
				messages.success(request, 'Your account with username |%s| has been created successfully today at  %s !!!.' % (username, now) )
				return redirect('/register/response')
			else:
				login_form = LoginForm()
				return render(request, "base.html", {        "title": title, 
					"form":login_form ,	
					"frm":form1 ,	
					'signuperrormessage':'Opps, Error encountered while trying to sign you up, Please try again!!'
					} )	
	return render(request, "base.html",{"form":login_form, 'frm':form1, "title": title,})


def upload_delete(request, upload_id):
	upload = MemberUpload.objects.get(pk=upload_id)
	upload.delete()
	uploads = MemberUpload.objects.filter(member_id=request.user)
	return redirect("BeginningDash:home")


def code_delete(request, code_id):
	code = UMCU.objects.get(pk=code_id)
	code.delete()
	codes = UMCU.objects.filter(user_id=request.user)
	return redirect("BeginningDash:code")


def AllFilesUploaded(request):
	title = "Files"
	return render(request, "Additions/AllFilesUpload.html", {"title":title})


def AllCodesUploaded(request):
	title = "Codes"
	return render(request, "Additions/AllCodesUpload.html", {"title":title})
	

def MediaUploaded(request):
	title = "Media"
	return render(request, "Additions/GalleryUpload.html", {"title":title})


class GeneratePDF(View):
	def get(self, request, *args, **kwargs):
		user_name = request.user
		item = MemberUpload.objects.filter(member=user_name)
		total_files = MemberUpload.objects.filter(member=user_name).all().count()
		total_vids = MemberUpload.objects.filter(member=user_name).values('VIDEO').exclude(VIDEO = '',).count()
		total_auds = MemberUpload.objects.filter(member=user_name).values('AUDIO').exclude(AUDIO = '',).count()
		total_imgs = MemberUpload.objects.filter(member=user_name).values('IMAGE').exclude(IMAGE = '',).count()
		total_pdfs = MemberUpload.objects.filter(member=user_name).values('PDF').exclude(PDF = '',).count()
		total_total = total_vids + total_auds + total_imgs + total_pdfs
		today = datetime.date.today()
		template = get_template('Additions/sumPDFtemp.html')
		context = {
			"invoice_id": 123,
			"member_name": user_name,
			"amount": 1399.99,
			"today": today,
			"item":item,
			"total_files":total_files,
			"total_vids":total_vids,
			"total_imgs":total_imgs,
			"total_pdfs":total_pdfs,
			"total_auds":total_auds,
			"total_total":total_total,
		}
		html = template.render(context)
		pdf = render_to_pdf('Additions/sumPDFtemp.html', context)
		if pdf:
			response = HttpResponse(pdf, content_type='application/pdf')
			filename = "%s_Upload_%s_for_%s.pdf" %(user_name,"Summary",today)
			content = "inline; filename=%s" %(filename)
			download = request.GET.get("download")
			if download:
				content = "attachment; filename='%s'" %(filename)
			response['Content-Disposition'] = content
			return response
		return HttpResponse("Not found")


class GeneratePDF_4_code(View):
	def get(self, request, *args, **kwargs):
		user_name = request.user
		item_4_code = UMCU.objects.filter(user=user_name)
		total_files_4_code = UMCU.objects.filter(user=user_name).all().count()
		total_html = UMCU.objects.filter(user=user_name).values('HTML').exclude(HTML = '',).count()
		total_css = UMCU.objects.filter(user=user_name).values('CSS').exclude(CSS = '',).count()
		total_total_4_code = total_html + total_css 
		today = datetime.date.today()
		template = get_template('Additions/sumPDFtempcode.html')
		context = {
			"invoice_id": 123,
			"member_name": user_name,
			"amount": 1399.99,
			"today": today,
			"item_4_code":item_4_code,
			"total_files_4_code":total_files_4_code,
			"total_html":total_html,
			"total_css":total_css,
			"total_total_4_code":total_total_4_code,
		}
		html = template.render(context)
		pdf = render_to_pdf('Additions/sumPDFtempcode.html', context)
		if pdf:
			response = HttpResponse(pdf, content_type='application/pdf')
			filename = "%s_Upload_%s_for_%s.pdf" %(user_name,"Summary",today)
			content = "inline; filename=%s" %(filename)
			download = request.GET.get("download")
			if download:
				content = "attachment; filename='%s'" %(filename)
			response['Content-Disposition'] = content
			return response
		return HttpResponse("Not found")


def aboutus(request):
	title = "About-us"
	return render(request, "Beginning/about.html", {"title":title})


def aboutfornonuser(request):
	title = "About-us"
	return render(request, "Beginning/about.html", {"title":title})


def mycontact(request,pk=None):
	if request.user.is_authenticated():
		usermail = request.user.email
		useremailname = request.user
		first_name = request.user.first_name
		last_name = request.user.last_name
		joined = request.user.date_joined
		emailTo = settings.EMAIL_HOST_USER
		myForm = ContactXForm(request.POST or None)
		confirm_message= None
		title = "Contact"
		title1 = "Contact"
		user = ''
		if request.method == "POST":
			subject = request.POST.get('subject')
			message = request.POST.get('message')
			emailFrom = request.POST.get("email")
			time = request.POST.get("sent_time")
			d = {
						"name": useremailname, 
						"first":first_name,
						"last":last_name, 
						"join":joined, 
						"mysubject":subject , 
						"mymessage":message, 
						"msg_time":time, 
						"myemail":emailFrom
			    }
			A = get_template('templated_email/contactemail.html')
			comment = 'Message : %s ; commented by %s;' % (message,useremailname )
			plaintext = get_template('templated_email/contactemail.html')
			htmly  = get_template('templated_email/contactemail.html')
			text_content = plaintext.render(d)
			html_content = htmly.render(d)
			msg = EmailMultiAlternatives(subject, text_content,emailFrom,[emailTo])
			msg.attach_alternative(html_content, "text/html")
			msg.send()
			title = 'ThankYou'
			title1 = " Thank You ! "
			confirm_message = "Thanks for Contacting  DashNG ~ Vs., We will get back to you real soon!!"
			form = None


		context = {
			"ContactXForm":myForm,
			'title':title,
			'title1':title1,
			'usermail':usermail,
			'first_name':first_name,
			'last_name':last_name,
			'confirm_message':confirm_message
		}
		return render(request, "Beginning/contact.html", context)
	else:
		myForm = ContactXForm(request.POST or None)
		confirm_message= None
		title = "Contact"
		title1 = "Contact"
		if request.method == "POST":
			subject = request.POST.get('subject')
			message = request.POST.get('message')
			emailFrom = request.POST.get("email")
			time = request.POST.get("sent_time")
			joined = request.user.date_joined
			emailTo = settings.EMAIL_HOST_USER
			d = {
						"name": useremailname,
						"first":first_name,
						"last":last_name,
						"join":joined,
						"mysubject":subject ,
						"mymessage":message,
						"msg_time":time,
						"myemail":emailFrom
			}
			A = get_template('templated_email/contactemail.html')
			comment = 'Message : %s ; commented by %s;' % (message,useremailname )
			plaintext = get_template('templated_email/contactemail.html')
			htmly  = get_template('templated_email/contactemail.html')
			text_content = plaintext.render(d)
			html_content = htmly.render(d)
			msg = EmailMultiAlternatives(subject, text_content,emailFrom,[emailTo])
			msg.attach_alternative(html_content, "text/html")
			msg.send()
			title = 'ThankYou'
			title1 = " Thank You ! "
			confirm_message = "Thanks for Contacting  DashNG ~ Vs., We will get back to you real soon!!"
			form = None
		context = {
			"ContactXForm":myForm,
			'title':title,
			'title1':title1,
			'usermail':usermail,
			'first_name':first_name,
			'last_name':last_name,
			'confirm_message':confirm_message
		}
		return render(request, "Beginning/contact.html", context)


def mycontact4offlineuser(request,pk=None):
	if not request.user.is_authenticated():
		usermail = "Anonymous"
		useremailname = "Anonymous (UNREGISTERED)"
		first_name = "Anonymous"
		last_name = "Anonymous"
		joined = "NOT JOINED YET"
		emailTo = settings.EMAIL_HOST_USER
		myForm = ContactXForm(request.POST or None)
		confirm_message= None
		title = "Contact"
		title1 = "Contact"
		user = ''
		if request.method == "POST":
			subject = request.POST.get('subject')
			message = request.POST.get('message')
			emailFrom = request.POST.get("email")
			time = request.POST.get("sent_time")
			d = {
						"name": useremailname,
						"first":first_name,
						"last":last_name,
						"join":joined,
						"mysubject":subject ,
						"mymessage":message,
						"msg_time":time,
						"myemail":emailFrom
			}
			A = get_template('templated_email/contactemail.html')
			comment = 'Message : %s ; commented by %s;' % (message,useremailname )
			plaintext = get_template('templated_email/contactemail.html')
			htmly  = get_template('templated_email/contactemail.html')
			text_content = plaintext.render(d)
			html_content = htmly.render(d)
			msg = EmailMultiAlternatives(subject, text_content,emailFrom,[emailTo])
			msg.attach_alternative(html_content, "text/html")
			msg.send()
			title = 'ThankYou'
			title1 = " Thank You ! "
			confirm_message = "Thanks for Contacting  DashNG ~ Vs., We will get back to you real soon!!"
			form = None
		context = {
			"ContactXForm":myForm,
			'title':title,
			'title1':title1,
			'usermail':usermail,
			'first_name':first_name,
			'last_name':last_name,
			'confirm_message':confirm_message
		}
		return render(request, "Beginning/contact.html", context)
	else:
		usermail = "Anonymous"
		myForm = ContactXForm(request.POST or None)
		confirm_message= None
		useremailname = "Anonymous (UNREGISTERED)"
		first_name = "Anonymous"
		last_name = "Anonymous"
		joined = "NOT JOINED YET"
		emailTo = settings.EMAIL_HOST_USER
		title = "Contact"
		title1 = "Contact"
		if request.method == "POST":
			subject = request.POST.get('subject')
			message = request.POST.get('message')
			emailFrom = request.POST.get("email")
			time = request.POST.get("sent_time")
			d = {
						"name": useremailname,
						"first":first_name,
						"last":last_name,
						"join":joined,
						"mysubject":subject ,
						"mymessage":message,
						"msg_time":time,
						"myemail":emailFrom
			}
			A = get_template('templated_email/contactemail.html')
			comment = 'Message : %s ; commented by %s;' % (message,useremailname)
			plaintext = get_template('templated_email/contactemail.html')
			htmly  = get_template('templated_email/contactemail.html')
			text_content = plaintext.render(d)
			html_content = htmly.render(d)
			msg = EmailMultiAlternatives(subject, text_content,emailFrom,[emailTo])
			msg.attach_alternative(html_content, "text/html")
			msg.send()
			title = 'ThankYou'
			title1 = " Thank You ! "
			confirm_message = "Thanks for Contacting  DashNG ~ Vs., We will get back to you real soon!!"
			form = None	
		context = {
			"ContactXForm":myForm,
			'title':title,
			'title1':title1,
			'usermail':usermail,
			'first_name':first_name,
			'last_name':last_name,
			'confirm_message':confirm_message
		}
		return render(request, "Beginning/contact.html", context)

def change_password(request):
	now = datetime.datetime.now()
	if request.method == 'POST':
		form = PasswordChangeForm(data=request.POST, user=request.user)
		if form.is_valid():
			form.save()
			update_session_auth_hash(request, form.user)
			messages.success(request, 'Your account password has been updated successfully today at  %s !!!.' % ( now) )
			return redirect(reverse("BeginningDash:view_profile"))
		else:
			return redirect(reverse("BeginningDash:change_password"))   
	else:
		form = PasswordChangeForm(user=request.user)
		args = {'form': form}
		return render(request, 'Beginning/change_password.html', args)



