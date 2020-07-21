from django.contrib import admin
from BeginningDash.models import ( 
	MemberUpload,
	UMCU,
	UserProfile, 
	NewsByAdmin,
	say_something_nice,
	ContactXModel,
)


class MemberUploadAdmin(admin.ModelAdmin):
	list_display = ('member', 'file_group','VIDEO', 'AUDIO', 'PDF','IMAGE','date_uploaded','comment')
	list_filter = ('member', 'file_group','VIDEO', 'AUDIO', 'PDF','IMAGE','comment')
	search_fields = ('file_group','VIDEO', 'AUDIO', 'PDF','IMAGE','comment')
	date_hierarchy = 'date_uploaded'
	ordering = ['date_uploaded']
admin.site.register(MemberUpload,MemberUploadAdmin)


class UMCUAdmin(admin.ModelAdmin):
	list_display = ('user','folder','HTML','CSS','uploaded_time','says')
	list_filter = ('user','folder','HTML','CSS','uploaded_time','says')
	search_fields = ('folder','HTML','CSS','uploaded_time','says')
	date_hierarchy = 'uploaded_time'
	ordering = ['uploaded_time']
admin.site.register(UMCU,UMCUAdmin)


class UserProfileAdmin(admin.ModelAdmin):
	list_display = ('user', 'city', 'phone','image')
	list_filter = ('city', 'user')
	search_fields = ('user', 'city', 'phone','image',)
admin.site.register(UserProfile,UserProfileAdmin) 


class NewsByAdminAdmin(admin.ModelAdmin):
	list_display = ('Name','Heading','id', 'News','date', 'time', 'importance')
	list_filter = ('Name','Heading','id', 'News','date', 'time', 'importance')
	search_fields = ('Name','Heading' ,'id','News','date', 'time', 'importance')
	date_hierarchy = 'date'
	ordering = ['date']
admin.site.register(NewsByAdmin,NewsByAdminAdmin)


class say_something_niceAdmin(admin.ModelAdmin):
	list_display = ('Name','Photo','Comment','Occupation', 'created','status')
	list_filter = ('Name','Photo','Comment','Occupation', 'created','status')
	search_fields = ('Name','Photo','Comment','Occupation', 'created','status')
admin.site.register(say_something_nice, say_something_niceAdmin)


class ContactXModelAdmin(admin.ModelAdmin):
	list_display = ('email','subject','message', 'sent_time')
	list_filter = ('email','subject','message', 'sent_time')
	search_fields = ('email','subject','message', 'sent_time')
admin.site.register(ContactXModel, ContactXModelAdmin)





