from django import forms
from cake.models import User,Category,Cakes,CakeVarients,Carts,Reviews,Orders
from django.contrib.auth.forms import UserCreationForm

class RegistrationForm(UserCreationForm):
    class Meta:
        model=User
        fields=["username","email","password1","password2","phone","address"]

class LoginForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField(widget=forms.PasswordInput)

class CategoryCreateForm(forms.ModelForm):
    class Meta:
        model=Category
        fields=["name"]

class CakeAddForm(forms.ModelForm):
    class Meta:
        model=Cakes
        fields="__all__"

class CakeVarientForm(forms.ModelForm):
    class Meta:
        model=CakeVarients
        exclude=("cake",)#cake=models.ForeignKey(Cakes,on_delete=models.CASCADE)
        
















