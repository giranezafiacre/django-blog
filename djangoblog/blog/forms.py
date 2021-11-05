from django import forms
from .models import Post


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