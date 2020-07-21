import re
from django import forms
from django.contrib.auth import (
     authenticate,
     login,
     logout
    )
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django import forms
from .models import *
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput( 
        attrs={'class':'form-control', 'placeholder':
        'Enter username'}), required=True,min_length=4, max_length=50)
    password = forms.CharField(widget=forms.PasswordInput( 
        attrs={'class':'form-control', 'placeholder':
        'Enter Password'}), required=True,min_length=4, max_length=50)
    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        if username and password :
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("This user does not exist")
            if not user.check_password(password):
                raise forms.ValidationError("Incorrect credentials")
            if not user.is_active:
                raise forms.ValidationError("This user is not longer active.")
        return super(LoginForm, self).clean(*args, **kwargs)


class RegisterForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput( 
        attrs={'class':'form-control', 'placeholder':
        'Enter username'}), required=True, max_length=50)

    email = forms.CharField(widget=forms.EmailInput( 
        attrs={'class':'form-control', 'placeholder':
        'Enter Email Address '}), required=True, max_length=50)

    first_name = forms.CharField(widget=forms.TextInput( 
        attrs={'class':'form-control', 'placeholder':
        'Enter first name'}), required=True, max_length=50)

    last_name = forms.CharField(widget=forms.TextInput( 
        attrs={'class':'form-control', 'placeholder':
        'Enter last name'}), required=True, max_length=50)

    password = forms.CharField(widget=forms.PasswordInput( 
        attrs={'class':'form-control', 'placeholder':
        'Enter Password'}), required=True, max_length=50)


    confirm_password = forms.CharField(widget=forms.PasswordInput( 
        attrs={'class':'form-control', 'placeholder':
        'Confirm password'}), required=True, max_length=50)

    class Meta():
        model = User
        fields = [
          'username',
          'email',
          'first_name',
          'last_name',
          "password",
          "confirm_password",
        ]
    def clean_username(self):
        user = self.cleaned_data['username']
        try:
            match = User.objects.get(username = user )
        except:
            return self.cleaned_data['username']
        raise forms.ValidationError('Username already exist')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        email_qs = User.objects.filter(email=email)
        if email_qs.exists():
            raise forms.ValidationError("This email has already been registered")
        return email

    def clean_confirm_password(self):
        pas = self.cleaned_data['password']
        cpas = self.cleaned_data['confirm_password']
        MIN_LENGTH = 8
        if pas and cpas:
            if pas != cpas:
                raise forms.ValidationError("Passord and Confirm Password do not Match ")
            else:
                if len(pas) < MIN_LENGTH:
                    raise forms.ValidationError("Password should have atleast %d characters" %MIN_LENGTH)
                if pas.isdigit():
                    raise ValidationError("Password Should not all be numeric ")


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = (
          'city',
          'phone',
          "image"   
        )


class UserEditForm(forms.ModelForm):
    class Meta:
      model = User
      fields = 'email', 'first_name', 'last_name'


class contactForm(forms.Form):  
    subject = forms.CharField( required=True,
      widget=forms.TextInput( attrs={'class':'form-control','placeholder':'Initiate a Subject'}) ,
      max_length=500, help_text='500 characters max.',
      label=("Subject")
    )

    comment = forms.CharField(required=True,
      widget=forms.Textarea( attrs={'class':'form-control','placeholder':'Enter your Message'}),
      label=(),
      help_text="""<div align="right" ><span style="color:green;"><i class="fa fa-arrow-circle-right" 
      aria-hidden="true"></i> Structure your Message Constructively.</span></div>
      """
    )
    email = forms.EmailField(required=True,
      widget=forms.TextInput( attrs={'class':'form-control','placeholder':'Enter your Email'}),
      label=(),
      help_text="""<div align="right" ><span style="color:green;"><i class="fa fa-arrow-circle-right" 
      aria-hidden="true"></i> Structure your Message Constructively.</span></div>
      """     
    )






 