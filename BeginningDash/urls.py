from django.conf.urls import url
from BeginningDash import views
from django.contrib.auth import views as myviews
from BeginningDash.views import GeneratePDF
from BeginningDash.views import GeneratePDF_4_code
from django.contrib.auth.models import User
from django.contrib.auth.views import (
	password_reset,
	password_reset_done, 
	password_reset_confirm,
	password_reset_complete
 )

app_name = 'BeginningDash'
urlpatterns = [
	url(r'^contact-us/', views.mycontact, name="contact"),
	url(r'^aboutus/', views.aboutus, name="aboutus"),
	url(r'^aboutfornonuser/', views.aboutfornonuser, name="aboutfornonuser"),
	url(r'^mycontact4offlineuser/', views.mycontact4offlineuser, name="mycontact4offlineuser"),
	url(r'^home/dashboard/$', views.homepage, name="home"),
	url(r'^coding/now/$', views.UCU, name="code"),
	url(r'^all/files/upload/$', views.AllFilesUploaded, name="allfiles"),
	url(r'^all/codes/upload/$', views.AllCodesUploaded, name="allcodes"),
	url(r'^media/upload/$', views.MediaUploaded, name="gallery"),
	url(r'^uploadpdf/$', GeneratePDF.as_view(),name="pdf"),
	url(r'^uploadpdf/code/$', GeneratePDF_4_code.as_view(),name="pdf_code"),
	url(r'^created_document/$', views.created_document, name='created_document'),
	url(r'^profile/$', views.view_profile, name="view_profile"),
	url(r'^user/profile/edit/$', views.edit_profile, name='edit_profile'),
	url(r'^account/logout/$', views.logout,name="logout"),
	url(r'^(?P<upload_id>[0-9]+)/delete/files$', views.upload_delete, name="delete_upload"),
	url(r'^(?P<code_id>[0-9]+)/delete/codes$', views.code_delete, name="delete_code"),
	url(r'^login-reg/', views.loginX_regX, name='loginX_regX'),	
	url(r'^register/response/', views.register_response, name='reg_response'),
	url(r'^change-password/$', views.change_password, name='change_password'),
	url(r'^reset-password/$', password_reset,
		{ "template_name":"Beginning/reset_password.html","post_reset_redirect":"BeginningDash:password_reset_done",
		"email_template_name":"Beginning/reset_password_email.html"},
		name='reset_password'),
	url(r'^reset-password/done/$', password_reset_done,{"template_name":"Beginning/reset_password_done.html"},name='password_reset_done'),
	url(r'^reset-password/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', password_reset_confirm,{"post_reset_redirect":"BeginningDash:password_reset_complete","template_name":"Beginning/reset_password_confirm.html"}, name='password_reset_confirm' ),
	url(r'^reset-password/complete/$', password_reset_complete,{"template_name":"Beginning/reset_password_complete.html"},name="password_reset_complete")
]


