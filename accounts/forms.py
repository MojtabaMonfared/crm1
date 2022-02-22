from django.db.models import fields
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

from .models import *


class CustomerForm(ModelForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['profile_pic'].widget.clear_checkbox_label = 'حذف'
		self.fields['profile_pic'].widget.initial_text = "تصویر موجود"
		self.fields['profile_pic'].widget.input_text = "تغییر"

	class Meta:
		model = Customer
		fields = '__all__'
		exclude = ['user']


# Order Form
class OrderForm(ModelForm):
	class Meta:
		model = Order
		fields = '__all__'


class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = [
			'username',
			'email',
			'password1',
			'password2'
		]