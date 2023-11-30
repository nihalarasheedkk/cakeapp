from typing import Any
from django.shortcuts import render

# Create your views here.
from django.db import models
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.views.generic import CreateView,FormView,ListView,UpdateView,DetailView
from django.urls import reverse_lazy,reverse
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.utils.decorators import method_decorator

from cake.forms import RegistrationForm,LoginForm,CategoryCreateForm,CakeAddForm,CakeVarientForm
from cake.models import User,Category,Cakes,CakeVarients

def signin_required(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            messages.error(request,"invalid session")
            return redirect("signin")
        else:
            return fn(request,*args,**kwargs)
    return wrapper

def is_admin(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            messages.error(request,"permission denied")
            return redirect("signin")
        else:
            return fn(request,*args,**kwargs)
    return wrapper

decs=[signin_required,is_admin]    

class RegisterView(CreateView):
    template_name="cake/register.html"
    form_class=RegistrationForm
    model=User
    success_url=reverse_lazy("login")

    def form_valid(self, form) :
        messages.success(self.request,"account created :)")
        return super().form_valid(form)
    def form_invalid(self, form) :
        messages.error(self.request,"failed to create account :)")
        return super().form_invalid(form)


class SignInView(FormView):
    template_name="cake/getin.html"
    form_class=LoginForm

    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)

        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            usr=authenticate(request,username=uname,password=pwd)
            if usr:
                login(request,usr)
                messages.success(request,"loginned successfully")
                return redirect("cake-add")
            else:
                messages.error(request,"invalid cred")
                return render(request,self.template_name,{"form":form})

@method_decorator(decs,name="dispatch")
class CategoryCreateView(CreateView,ListView) :
    template_name="cake/category_add.html" 
    form_class=CategoryCreateForm
    model=Category
    context_object_name="categories"  
    success_url=reverse_lazy("add-category")
    def form_valid(self, form) :
        messages.success(self.request,"category added successfully")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request,"category adding failed")
        return super().form_invalid(form)
    
    def get_queryset(self) :
        return Category.objects.filter(is_active=True)
    
@signin_required
@is_admin
def remove_category(request,*args,**kwargs):
    id=kwargs.get("pk")
    Category.objects.filter(id=id).update(is_active=False)
    messages.success(request,"category removed")
    return redirect("add-category")

@method_decorator(decs,name="dispatch")
class CakeCreateView(CreateView):

    template_name="cake/cake_add.html"
    model=Cakes
    form_class=CakeAddForm
    success_url=reverse_lazy("cake-add")

    def form_valid(self, form):
        messages.success(self.request,"cake has been added")
        return super().form_valid(form)
    def form_invalid(self, form) :
        messages.error(self.request,"cloth addin failed")
        return super().form_invalid(form)
    
@method_decorator(decs,name="dispatch")
class CakeListView(ListView):
    template_name="cake/cake_list.html"
    model=Cakes
    context_object_name="cakes"

@signin_required
@is_admin
def remove_cakeview(request,*args,**kwargs):
    id=kwargs.get("pk")
    Cakes.objects.filter(id=id).delete()
    return redirect("cake-list")    

@method_decorator(decs,name="dispatch")
class CakeVarientView(CreateView):
    template_name="cake/cakevarient_add.html"
    form_class=CakeVarientForm
    model=CakeVarients
    success_url=reverse_lazy("cake-list")

    def form_valid(self, form):
        id=self.kwargs.get("pk")
        obj=Cakes.objects.get(id=id)
        form.instance.cake=obj
        messages.success(self.request,"varient has added")
        return super().form_valid(form)
    
@method_decorator(decs,name="dispatch")
class CakeDetailView(DetailView):
    template_name="cake/cake_detail.html"
    model=Cakes  
    context_object_name="cake"  

@method_decorator(decs,name="dispatch")
class CakeUpdateView(UpdateView):
    template_name="cake/cake_edit.html"
    model=Cakes
    form_class=CakeAddForm
    success_url=reverse_lazy("cake-list")
    def form_valid(self, form) :
        messages.success(self.request,"cloth updated")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request,"cloth update failed")
        return super().form_invalid(form)
    
@method_decorator(decs,name="dispatch")
class CakeVarientUpdateView(UpdateView):
    template_name="cake/cakevarient_edit.html" 
    model=CakeVarients
    form_class=CakeVarientForm
    success_url=reverse_lazy("cake-list")
    def form_valid(self, form):
        messages.success(self.request,"cloth varient added")
        return super().form_valid(form)
    def form_invalid(self, form):
        messages.error(self.request,"cloth varient updated")
        return super().form_invalid(form)
    def get_success_url(self) :
        id=self.kwargs.get("pk")
        cake_varient_object=CakeVarients.objects.get(id=id)
        cake_id=cake_varient_object.cake.id
        return reverse("cake-detail",kwargs={"pk":cake_id})
    
@signin_required
@is_admin

def remove_varient(request,*args,**kwargs):
    id=kwargs.get("pk")
    CakeVarients.objects.filter(id=id).delete()
    return redirect("cake-list")
    

