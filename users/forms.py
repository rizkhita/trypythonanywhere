from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
# officials = (
#         ('Liputan6', 'Liputan6'),
#         ('Kompas', 'Kompas'),
#         ('PikiranRakyat', 'PikiranRakyat'),
#         ('Unofficial', 'Unofficial'),
#     )

# gends = [('M','Male'),('F','Female')]

class UserRegisterForm(UserCreationForm):
	"""docstring for ClassName"""
	# add this one
	email = forms.EmailField()
	## min 37.49
	# gender = forms.ChoiceField(choices=gends,label="gender")
	## bodo amat ini kan latihan
	# topic_interest = forms.MultiSelectField(CHOICE=?)

	# add 

	class Meta:
		model = User
		fields = ['username','email','password1','password2']


class UserUpdateForm(forms.ModelForm):
	email = forms.EmailField()

	class Meta:
		model = User 
		fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):

	class Meta:
		model = Profile
		fields = ['image']