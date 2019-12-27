from django import forms


class SubmitForm(forms.Form):
    title = forms.CharField(label='Title', max_length=128)
    url = forms.URLField(required=False)
    text = forms.CharField(label="Text", widget=forms.Textarea, required=False)


class LoginForm(forms.Form):
    username = forms.CharField(label="username")
    password = forms.CharField(label="password", widget=forms.PasswordInput)
