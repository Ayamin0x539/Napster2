import re
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
 
class RegistrationForm(forms.Form): 
    username = forms.RegexField(regex=r'^\w+$', widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=_("Username"), error_messages={ 'invalid': _("This value must contain only letters, numbers and underscores.") })
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=_("Email address"))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)), label=_("Password"))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)), label=_("Password (again)"))
 
    def clean_username(self):
        try:
            user = User.objects.get(username__iexact=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError(_("The username already exists. Please try another one."))
 
    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_("The two password fields did not match."))
        return self.cleaned_data

class AccountManagementForm(forms.Form):
#    password1 = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)), label=_("Password"))
    firstname = forms.CharField(label='First Name', max_length=40)
    lastname = forms.CharField(label='Last Name', max_length=20)
    phone = forms.CharField(label='Phone Number', max_length=60)
    email = forms.CharField(label='Email', max_length=30)
    postalcode = forms.CharField(label='Zip/Postal Code', max_length=10)
    address = forms.CharField(label='Address', max_length = 70)
    city = forms.CharField(label='City', max_length=40)
    state = forms.CharField(label='State', max_length=40)
    country = forms.CharField(label='Country', max_length=45)
    fax = forms.CharField(label='Fax', max_length=45)
    # payment info
    creditcardnumber = forms.CharField(label='Credit Card Number', max_length=16)
    paypalemail = forms.CharField(label='Paypal Email', max_length=30)
    googlepayid = forms.CharField(label='GooglePay ID', max_length=30)
    applepayid = forms.CharField(label='AppleID (ApplePay)', max_length=30)

class EditPaymentsForm(forms.Form):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)), label=_("Password"))    

class EmployeeEnterNewMediaForm(forms.Form):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)), label=_("Password"))    

class AdministratorRunReportForm(forms.Form):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)), label=_("Password"))    

class AdministratorEmployeeProductivityForm(forms.Form):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)), label=_("Password"))    

class OrderForm(forms.Form):
    orderid = forms.IntegerField()  
    customerid = forms.IntegerField()  
    playlistmadby = forms.CharField()  
    price = forms.CharField()  
