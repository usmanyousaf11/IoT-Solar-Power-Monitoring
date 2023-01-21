from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms



from .models import Order
from .models import crudinv
from .models import crudmodbus


class invform(forms.ModelForm):
    class Meta:
        model=crudinv
        fields="__all__"

class mbform(forms.ModelForm):
    class Meta:
        model=crudmodbus
        fields="__all__"


class OrderForm(ModelForm):
	class Meta:
		model = Order
		fields = '__all__'

class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']

