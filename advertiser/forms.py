from django import forms
from .views import *

from api.models import Advertisement
import datetime





class RegistrationForm(forms.Form):
    username = forms.CharField(required=True, max_length=25)
    password = forms.CharField(widget=forms.PasswordInput, label='Password', required=True)
    confirmpassword = forms.CharField(widget=forms.PasswordInput, label='Confirm Password', required=True)
    email = forms.CharField(label='Email Address', required=True)
    phone = forms.CharField(max_length=25, required=True)
    username.widget = forms.TextInput(attrs={'placeholder': 'Username'})
    password.widget = forms.PasswordInput(attrs={'placeholder': 'Password'})
    confirmpassword.widget = forms.PasswordInput(attrs={'placeholder': 'Confirm Password'})
    phone.widget = forms.PasswordInput(attrs={'placeholder': 'Phone'})
    email.widget = forms.EmailInput(attrs={'placeholder': 'Email', 'width': 20})


class AdvertisementForm(forms.ModelForm):
    class Meta:
        model = Advertisement
        exclude = ['advertiser']
        fields = '__all__'


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=20, required=True)
    username.widget = forms.TextInput(attrs={'placeholder': 'Username'})
    password = forms.CharField(widget=forms.PasswordInput, required=True, label='Password')
    password.widget = forms.PasswordInput(attrs={'placeholder': 'Password'})


OPTIONS = [
    ("0", "*ALL"),
    ("1", "Sport"),
    ("2", "Technology"),
]


class Userinput(forms.Form):



    name = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'name' , ' class':'form-control1'}))
    description = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'description' , ' class':'form-control1'}))
    pub_date = forms.DateField(initial=datetime.date.today,required=True, widget=forms.TextInput(attrs={'placeholder': 'pub_date' , ' class':'form-control1'}))
    max_age = forms.IntegerField(required=True, widget=forms.TextInput(attrs={'placeholder': 'max_age' , ' class':'form-control1'}))
    min_age = forms.IntegerField(required=True, widget=forms.TextInput(attrs={'placeholder': 'min_age' , ' class':'form-control1'}))
    # category = forms.CharField(label='What is your favorite fruit?', widget=forms.Select(choices=FRUIT_CHOICES))
    # category = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=OPTIONS)

    category = forms.MultipleChoiceField(
        choices=OPTIONS,
        initial='0',
        widget=forms.SelectMultiple(attrs={' class':'js-example-basic-multiple'}),
        required=True,
        label='Office'

    )


class EmailForm(forms.Form):
    email = forms.CharField(label='Email Address', required=True)
    email.widget = forms.EmailInput(attrs={'placeholder': 'Email'})

class changeForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput, label='Password', required=True)
    confirmpassword = forms.CharField(widget=forms.PasswordInput, label='Confirm Password', required=True)
    username = forms.CharField(required=True, max_length=25)
    password.widget = forms.PasswordInput(attrs={'placeholder': 'Password'})
    confirmpassword.widget = forms.PasswordInput(attrs={'placeholder': 'Confirm Password'})
    username.widget = forms.TextInput(attrs={'placeholder': 'Username'})

class update(forms.Form):
    name = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'name'}))
    description = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'description'}))
