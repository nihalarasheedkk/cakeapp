from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):

    phone=models.CharField(max_length=100,unique=True)
    address=models.CharField(max_length=200)


class Category(models.Model):

    name=models.CharField(max_length=200,unique=True)
    is_active=models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
class Cakes(models.Model):
    name=models.CharField(max_length=200)
    options=(
        ("choclate cake","choclate cake"),
        ("butterscotch","butterscotch"),
        ("red velvet","red velvet"),
        ("milk cake","milk cake"),
        ("cheese cake","cheese cake"),
        ("cup cake","cup cake")
    )
    material=models.CharField(max_length=200,choices=options,default="choclate cake")
    image=models.ImageField(upload_to="images")
    brand=models.CharField(max_length=200)
    
    Category=models.ForeignKey(Category,null=True,on_delete=models.SET_NULL)#on_delete=set null

    def __str__(self):
        return self.name

class CakeVarients(models.Model):
    price=models.PositiveIntegerField()
    color=models.CharField(max_length=100)
    options=(
        ("half kg","half kg"),
        ("one kg","one kg")
        
    )

    size=models.CharField(max_length=200,choices=options,default="one kg")
    cake=models.ForeignKey(Cakes,on_delete=models.CASCADE)

# class Offers(models.Model):
#     clothvarient=models.ForeignKey(ClothVarients,on_delete=models.CASCADE)
#     price=models.PositiveIntegerField()
#     start_date=models.DateTimeField()
#     due_date=models.DateTimeField()


class Carts(models.Model):
    cakevarient=models.ForeignKey(CakeVarients,on_delete=models.DO_NOTHING)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    options=(
        ("in-cart","in-cart"),
        ("order-placed","order-placed"),
        ("cancelled","cancelled")
    )

    status=models.CharField(max_length=200,choices=options,default="in-cart")
    date=models.DateTimeField(auto_now_add=True)


class Orders(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    cakevarient=models.ForeignKey(CakeVarients,on_delete=models.CASCADE)
    options=(
      
        ("order-placed","order-placed"),
        ("cancelled","cancelled"),
        ("dispatced","dispatched"),
        ("in-transit","in-transit"),
        ("delivered","delivered")
    )
    status=models.CharField(max_length=200,choices=options,default="order-placed")
    orderd_date=models.DateTimeField(auto_now_add=True)
    expected_date=models.DateField(null=True)
    address=models.CharField(max_length=200)

from django.core.validators import MinValueValidator,MaxValueValidator

class Reviews(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    cakevarient=models.ForeignKey(CakeVarients,on_delete=models.CASCADE)
    rating=models.PositiveIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    comment=models.CharField(max_length=300)

    




    


    






