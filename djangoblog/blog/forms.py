from django import forms
from .models import Comment, Post
from django.core.exceptions import ValidationError


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