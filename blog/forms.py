from django import forms
from .models import Comment, Post
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User


# creating a form
class Postform(forms.ModelForm):
    
	# create meta class
	class Meta:
		# specify model to be used
		model = Post

		# specify fields to be used
		fields = [
			"title",
			"content",
            "image"
		]

		
class Updateform(forms.ModelForm):
 
	# create meta class
	class Meta:
		# specify model to be used
		model = Post

		# specify fields to be used
		fields = [
			"title",
			"content",
            "image"
		]

class createComment(forms.ModelForm):

	# create meta class
	class Meta:
		# specify model to be used
		model = Comment

		# specify fields to be used
		fields = [
			"content"
		]


class CreateUserForm(UserCreationForm):
    class Meta:
        model=User
        fields = ['username','email','password1','password2']

class LoginForm(AuthenticationForm):
	class Meta:
		model=User
		fields=['username','password']