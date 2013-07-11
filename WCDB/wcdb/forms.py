from django import forms

class LoginForm(forms.Form) :
	username = forms.CharField(max_length=100)
	password = forms.CharField(max_length=100)

class UploadFileForm(forms.Form) :
	title = forms.CharField(max_length=50)
	file  = forms.FileField() 
