from django import forms
from .models import Resume, Job
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm




class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )

class ResumeUploadForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['file']
        widgets = {
            'file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'file': 'Upload Resume (.pdf or .docx)',
        }


class JobCreateForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'required_skills']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Python Developer'}),
            'required_skills': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Comma-separated skills (e.g. Python, Django, REST)'}),
        }
        labels = {
            'title': 'Job Title',
            'required_skills': 'Required Skills',
        }


class SkillFilterForm(forms.Form):
    skill = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Filter resumes by skill (optional)...'
        }),
        label=''
    )
