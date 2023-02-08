from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django import forms
from .models import Customer, BillingAddress, Product

class RegisterForm(UserCreationForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'placeholder': 'Username'}), min_length=2, max_length=100, error_messages={
        'required': 'This field is required!',
        'min_length': 'This username is too short!','max_length': 'This username is too long!',
        'unique': 'Username already exists!'
    })
    email = forms.EmailField(label='Email', widget=forms.TextInput(attrs={'placeholder': 'Email'}), error_messages={
        'required': 'This field is required!',
        'invalid': 'Please enter a valid email address!'
    })
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class ProfileSettingForm(UserChangeForm):
    password = None

    username = forms.CharField(label='Username', widget=forms.TextInput(), min_length=2, max_length=100, error_messages={
        'required': 'This field is required!',
        'min_length': 'This username is too short!','max_length': 'This username is too long!',
        'unique': 'Username already exists!'
    })
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

class CustomerForm(forms.ModelForm):
    
    class Meta:
        model = Customer
        fields = ('profile_image',)

class BillingAddressForm(forms.ModelForm):
    first_name = forms.CharField(label='First Name', widget=forms.TextInput(attrs={'placeholder': 'John'}), error_messages={
        'required': 'This field is required!'
    })
    last_name = forms.CharField(label='Last Name', widget=forms.TextInput(attrs={'placeholder': 'Doe'}), error_messages={
        'required': 'This field is required!'
    })
    email = forms.EmailField(label='Email', widget=forms.TextInput(attrs={'placeholder': 'example@email.com'}), error_messages={
        'required': 'This field is required!',
        'invalid': 'Please enter a valid email address!'
    })
    mobile_no = forms.CharField(label='Mobile No', widget=forms.TextInput(attrs={'placeholder': '+123 456 789'}), error_messages={
        'required': 'This field is required!'
    })
    address_line_one = forms.CharField(label='Address Line 1', widget=forms.TextInput(attrs={'placeholder': '123 Street'}), error_messages={
        'required': 'This field is required!'
    })
    address_line_two = forms.CharField(label='Address Line 2', widget=forms.TextInput(attrs={'placeholder': '123 Street'}), error_messages={
        'required': 'This field is required!'
    })
    country = forms.CharField(label='Country', widget=forms.TextInput(attrs={'placeholder': 'United States'}), error_messages={
        'required': 'This field is required!'
    })
    city = forms.CharField(label='City', widget=forms.TextInput(attrs={'placeholder': 'New York'}), error_messages={
        'required': 'This field is required!'
    })
    state = forms.CharField(label='State', widget=forms.TextInput(attrs={'placeholder': 'New York'}), error_messages={
        'required': 'This field is required!'
    })
    zip_code = forms.IntegerField(label='Zip Code', widget=forms.NumberInput(attrs={'placeholder': '123'}), error_messages={
        'required': 'This field is required!'
    })

    class Meta:
        model = BillingAddress
        fields = '__all__'
        exclude = ['order']
