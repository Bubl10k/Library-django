from django import forms
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Row, Column, Layout

from .models import Profile


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'firstname', 
                  'lastname', 'bio', 'birth_date']
    
    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.fields['birth_date'] = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
        self.helper = FormHelper(self)
        
        self.helper.layout = Layout(
            Row(
                Column('firstname', css_class='col-md-4'),
                Column('lastname', css_class='col-md-4'),
                Column('image', css_class='col-md-4'),
            ),
            Row(
                Column('bio', css_class='col-md-12')
            ),
            Row(
                Column('birth_date', css_class='col-md-4'),
            ),
        )
        

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label='Repeat password',
        widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']
        