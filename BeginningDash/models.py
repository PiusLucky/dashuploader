from django.db import models
from django.forms import ModelForm
from django import forms
from django.conf import settings
from django.contrib.auth.models import Permission, User
from .formatChecker import ContentTypeRestrictedFileField
from django.db.models.signals import post_save
from django.urls import reverse
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _ 
from django.db.models import Count

""""
File Sizes MB to Bytes
  2.5MB - 2621440
  5MB - 5242880
  10MB - 10485760
  20MB - 20971520
  50MB - 52428800
  100MB - 104857600
  250MB - 214958080
  500MB - 429916160
"""

def upload_location_Site_Evaluator_image(objects, filename):
    return '{0}/{1}/'.format(objects.Name,filename)
   
class EvaluationManager(models.Manager):
    def my_get_queryset(self):
        return super(EvaluationManager,self).my_get_queryset()\
        .filter(status='published')

# only if you need to support Python 2
@python_2_unicode_compatible 
class MemberUpload(models.Model):
    member = models.ForeignKey(User)
    file_group = models.CharField(max_length=100 )
    comment = models.CharField(max_length=1000, default= '')
    date_uploaded = models.DateTimeField(auto_now=False, auto_now_add=True)
    VIDEO = ContentTypeRestrictedFileField(upload_to= 'uploads', 
    	content_types=['video/mp4',],
    	max_upload_size=214958080,blank=True, null=True,db_index=True

    	)
    AUDIO = ContentTypeRestrictedFileField(upload_to= 'uploads', 
    	content_types=[ 'audio/mpeg', ],
    	max_upload_size=104857600,blank=True, null=True
    	)
    PDF = ContentTypeRestrictedFileField(upload_to= 'uploads', 
    	content_types=['application/pdf',  ],
    	max_upload_size=52428800,blank=True, null=True

    	)
    IMAGE = ContentTypeRestrictedFileField(upload_to= 'uploads', 
    	content_types=['image/jpeg', ],
    	max_upload_size=104857600,blank=True, null=True
    	)

    def __str__(self):
      return '%s uploaded in %s' % (self.member,self.file_group)
    def vids(self):
      return self.VIDEO
    def auds(self):
      return self.AUDIO
    def imgs(self):
      return self.IMAGE
    def pdfs(self):
      return self.PDF
    def creates(self):
      return self.date_uploaded
    def file_g(self):
      return self.file_group 
    class Meta:
      ordering = ('-date_uploaded',)
      verbose_name = 'MemberUpload'
      verbose_name_plural = 'MemberUploads'

class UMCU(models.Model):
    user = models.ForeignKey(User)
    folder = models.CharField(max_length=100 )
    says = models.CharField(max_length=1000, default= '')
    uploaded_time = models.DateTimeField(auto_now=False, auto_now_add=True)
    HTML = ContentTypeRestrictedFileField(upload_to= 'uploads', 
      content_types=['text/html', ], max_upload_size=52428800,blank=True, null=True    
    )
    CSS =  ContentTypeRestrictedFileField(upload_to= 'uploads', 
      content_types=['text/css', ], max_upload_size=52428800,blank=True, null=True
    )
    def __str__(self):
      return 'Code uploaded in %s at %s' % (self.folder, self.uploaded_time)
    def html(self):
      return self.HTML
    def css(self):
      return self.CSS
    def code_creates(self):
      return self.uploaded_time
    def file_g_4_code(self):
      return self.folder
    class Meta:
      ordering = ('-uploaded_time',)
      verbose_name = 'MemberCodeUpload'
      verbose_name_plural = 'MemberCodeUploads'


class UMCUForm(forms.ModelForm): 
    folder = forms.CharField(widget=forms.TextInput(
      attrs={'class': 'form-control', 'placeholder':'Insert Your Folder Name ....'}), required=True, label="MY FOLDER")
    says = forms.CharField(widget=forms.Textarea(
      attrs={'class': 'form-control', 'placeholder':'Quick Note...'}), required=False, label="COMMENT")
    class Meta:
        model = UMCU
        fields = [
          'folder',         
          'HTML',
          'CSS',
          'says',
        ]
class ContactXModel(models.Model):
    subject = models.CharField(max_length=300, default= '')
    email = models.EmailField(max_length=100)
    message = models.CharField(max_length=1000, default= '')
    sent_time = models.DateTimeField(auto_now=False, auto_now_add=True)
    def __str__(self):
        return 'Message: %s ::: sent @  %s  ' % (self.message, self.sent_time)

    class Meta:
        ordering = ('-sent_time',)
        verbose_name = 'ContactForm'
        verbose_name_plural = 'ContactForm'

class ContactXForm(forms.ModelForm): 
    subject = forms.CharField(widget=forms.TextInput(
      attrs={'class': 'form-control', 'placeholder':'Initiate a subject ....'}), required=True, label="Subject")
    email = forms.EmailField(widget=forms.TextInput(
      attrs={'class': 'form-control', 'placeholder':'Kindly use a valid email you want the admin to reply to!'}), required=True, label="Email")
    message = forms.CharField(widget=forms.Textarea(
      attrs={'class': 'form-control', 'placeholder':'Quick Note...'}), required=False, label="Message")

    class Meta:
        model = ContactXModel
        fields = [
          'subject',         
          'email',
          'message',
        ]

class NewsByAdmin(models.Model):
    Name = models.CharField(max_length=50, blank=False, null=False)
    Heading = models.CharField(max_length=50, blank=False, null=False)
    News = models.TextField(max_length=10000,blank=False, null=False, default= '')
    date = models.DateField(auto_now=False, auto_now_add=True)
    time = models.TimeField(auto_now=False, auto_now_add=True)
    importance = models.CharField(max_length=50, choices=(  
      ('Free Users', _('Free Users.')), 
      ('Premium Users', _('Premium Users')),
      ('Both Free And Premium Users', _('Both Free And Premium Users'))  
      )  
    ) 

    def __str__(self):
        return 'News By %s' % (self.Name)
    class Meta:
      ordering = ["-time", "-date"] 
      verbose_name = 'NewsByAdmin'
      verbose_name_plural = 'NewsByAdmins'


class say_something_nice(models.Model):
    ChooseEvaluationToShow  = (
           ('show', 'Show'),
           ('hide', 'Hide'),
    ) 
    Name = models.CharField(max_length=50, blank=False, null=False)
    Comment = models.TextField(max_length=200, blank=False, null=False)
    Occupation = models.CharField(max_length=50, blank=False, null=False)
    Photo = models.ImageField(upload_to=upload_location_Site_Evaluator_image, 
      null=False, 
      blank=False, 
      width_field="userwidth_field", 
      height_field="userheight_field",
      help_text = '** Reviews With Uploaded Face-Images are Usually Displayed **'
    )
    userheight_field = models.IntegerField(default=100)
    userwidth_field = models.IntegerField(default=100)
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=34,                              
      choices = ChooseEvaluationToShow,                              
      default='hide')
    published = EvaluationManager()
    def __str__(self):
        return 'Comment By %s' % (self.Name)
    class Meta:
      ordering = ('-created',)  
      verbose_name = 'say_something_nice'
      verbose_name_plural = 'say_something_nice'


class say_something_nice_Form(ModelForm):
    Name = forms.CharField(widget=forms.TextInput(
      attrs={'class': 'form-control', 'placeholder':'Surname then Firstname e.g Pius Lucky as  Pius L.'}), required=True, label="Name")
    Occupation = forms.CharField(widget=forms.TextInput(
      attrs={'class': 'form-control', 'placeholder':'Your Occupation e.g Teacher '}), required=True, label="Occupation")
    Comment = forms.CharField(widget=forms.Textarea(
    attrs={'class': 'form-control', 'placeholder':'Make A Review ( NB: Not more than 100 Characters )'}), required=True, label="Evaluation")
    class Meta:
        model = say_something_nice
        fields = [
        'Name',
        'Occupation',
        'Comment',
        'Photo',
        ]
class MemberUploadForm(ModelForm):
    file_group = forms.CharField(widget=forms.TextInput(
    attrs={'class': 'form-control', 'placeholder':'Insert Your Folder Name ....'}), required=True, label="MY FOLDER")

    comment = forms.CharField(widget=forms.Textarea(
    attrs={'class': 'form-control', 'placeholder':'Quick Note...'}), required=False, label="COMMENT")
    class Meta:
        model = MemberUpload
        fields = [
            'file_group',
            'VIDEO',
            'AUDIO',
            'PDF',
            'IMAGE',
            'comment',
        ]


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    city = models.CharField(max_length=100, default='', blank=True)
    phone = models.CharField(max_length=20, default='', blank=True)
    image = models.ImageField(null=True, blank=True)
    def __str__(self):
        return self.user.username

def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = UserProfile.objects.create(user=kwargs['instance'])

post_save.connect(create_profile, sender=User)





	



