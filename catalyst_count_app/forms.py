from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, PasswordChangeForm
from django.contrib.auth.models import User
from django.utils.translation import gettext, gettext_lazy as _
from django.core.exceptions import ValidationError


class UserRegistrationForm(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Password'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Confirm Password'}))
    email = forms.CharField(required=True, widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Email'}))
    

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        lables = {'email':'Email'}
        widgets = {'username':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Username'})}

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise ValidationError("An user with this email already exists!")
        return email  

    def clean_username(self):
        username = self.cleaned_data["username"]
        if User.objects.filter(username=username).exists():
            raise ValidationError("An user with this username already exists!")
        return username  
        
class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus':True, 'class':'form-control'}))
    password = forms.CharField(label=_("Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'current-password', 'class':'form-control'}))



class UploadFileDataForm(forms.Form):
    file = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'}),
        required=True,
        error_messages={'required': 'Please select a file to upload.'}
    )

    def clean_file(self):
        uploaded_file = self.cleaned_data.get('file')
        if uploaded_file:
            if not uploaded_file.name.endswith('.csv'):
                raise ValidationError('Invalid file format. Only CSV files are accepted.')

            max_size_mb = 1024  # 1 GB = 1024 MB
            if uploaded_file.size > max_size_mb * 1024 * 1024:
                raise ValidationError(f'File size exceeds {max_size_mb} MB. Please upload a smaller file. Your file size {uploaded_file.size} MB.')

        return uploaded_file

