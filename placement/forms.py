from django import forms
from .models import signup,studentData,company_details,training_skill
from django.core.exceptions import ValidationError
from django.contrib import messages
import re

class RegisterForms(forms.ModelForm):
    confirm_password = forms.CharField(max_length=200, widget=forms.PasswordInput())
    class Meta:
        model =signup
        fields =('username','email','password','confirm_password')
        widgets ={
                'password':forms.PasswordInput
        }

    def clean(self):
        super(RegisterForms,self).clean()
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if len(username) < 3:

            self.errors['username']=self.error_class(['Username should be of minimum 3 characters'])
        if len(password) < 8:
            self.errors['password'] = self.error_class(['Password should be minimum of 8 characters'])
        if not re.findall('\d',password):
            self.errors['password'] = self.error_class(['Password should contain atleast 1 digit'])
        if not re.findall('[A-Z]',password):
            self.errors['password'] = self.error_class(['Password should contain atleast 1 uppercase letter'])
        if not re.findall('[@#$&]',password):
            self.errors['password'] = self.error_class(['Password should contain atleast 1 of these @,#,$,& special characters'])
        if confirm_password != password:
            self.errors['password']=self.error_class(['Password and Confirm Password are not equal'])


    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(RegisterForms, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class studendDataForm(forms.ModelForm):
    class Meta:
        model = studentData
        exclude = ['user']
        fields ='__all__'
    
class companyDetailsForm(forms.ModelForm):
    class Meta:
        model= company_details
        fields = '__all__'


class training_form(forms.ModelForm):
    class Meta:
        model = training_skill
        exclude=['user']
        fields = '__all__'
