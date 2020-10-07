from django.db import models
from django.core.validators import MinLengthValidator
import datetime

from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    
    def __str__(self):
        return self.name

class NewCustomer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    address = models.CharField(max_length=100,  null=True)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    password = models.CharField(max_length=500)

    def register(self):
        self.save()

    @staticmethod
    def get_NewCustomer_by_email(email):
        try:
            return NewCustomer.objects.get(email=email)
        except:
            return False


    def isExists(self):
        if NewCustomer.objects.filter(email = self.email):
            return True

        return  False

class Category(models.Model):
    name = models.CharField(max_length=20)
    @staticmethod
    def get_all_categories():
        return Category.objects.all()

    def __str__(self):
        return self.name


class Seller(models.Model):
    first_name = models.CharField(max_length=50,  null=True)
    last_name = models.CharField(max_length=50,  null=True)
    address = models.CharField(max_length=100,  null=True)
    phone = models.CharField(max_length=15,  null=True)
    email = models.EmailField()
    password = models.CharField(max_length=500,  null=True)

    def register(self):
        self.save()

    @staticmethod
    def get_Seller_by_email(email):
        try:
            return Seller.objects.get(email=email)
        except:
            return False   

    def isExists(self):
        if Seller.objects.filter(email = self.email):
            return True        

class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    digital = models.BooleanField(default=False, null=True, blank=False)
    image = models.ImageField(null=True, blank=True)
    
    def __str__(self):
        return self.name  
    @property  
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url=''
        return url  

    @staticmethod
    def get_products_by_id(ids):
        return Product.objects.filter(id__in =ids)

    @staticmethod
    def get_all_products():
        return Product.objects.all()    

    @staticmethod
    def get_all_products_by_categoryid(category_id):
        if category_id:
            return Product.objects.filter(category = category_id)
        else:
            return Product.get_all_products();     

                      

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    date_orderd = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.id)

    @property 
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
           if i.product.digital == False:
               shipping = True
        return shipping       
    @property
    def get_cart_total(self):
        Orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in Orderitems])    
        return total

    @property
    def get_cart_items(self):
        Orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in Orderitems])    
        return total              

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total
 

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    zipcode = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.address   
    

class PreviousOrder(models.Model):
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer,
                                 on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField()
    address = models.CharField(max_length=50, default='', blank=True)
    phone = models.CharField(max_length=50, default='', blank=True)
    date = models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)

    def placeOrder(self):
        self.save()

    @staticmethod
    def get_orders_by_customer(customer_id):
        return PreviousOrder.objects.filter(customer=customer_id).prevoiusorder_by('-date')


