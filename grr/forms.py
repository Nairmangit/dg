from django import forms

class LogForm(forms.Form):
    login = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'size':30 , 'class':'form-control'}))
    password = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'size':30, 'type' : 'password', 'class' : 'form-control',  'id' : 'inputPassword'}))


class Form(forms.Form):
    date = forms.CharField(widget=forms.TextInput({'type' : 'date'}))

class Panel(forms.Form):
    comand = forms.CharField()
