from django import forms
from django.contrib.auth.models import User


class SubmitForm(forms.Form):
    title = forms.CharField(label='Title', max_length=128)
    url = forms.URLField(required=False)
    text = forms.CharField(label="Text", widget=forms.Textarea, required=False)


class LoginForm(forms.Form):
    username = forms.CharField(label="username")
    password = forms.CharField(label="password", widget=forms.PasswordInput)


class CommentForm(forms.Form):
    text = forms.CharField(label="", widget=forms.Textarea(attrs={'cols': '80', 'rows': '6'}))


class RegisterForm(forms.Form):
    username = forms.CharField(label="username")
    password = forms.CharField(label="password", widget=forms.PasswordInput)
    confirm_password = forms.CharField(label="password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        print(password)
        print(confirm_password)

        if password != confirm_password:
            raise forms.ValidationError("Passwords don't match")

        return cleaned_data
