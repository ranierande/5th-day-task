from django.contrib import admin
from .models import *


class AdminProduct(admin.ModelAdmin):
    list_display = ['name', 'price']



class AdminCategory(admin.ModelAdmin):
    list_display = ['name']



class AdminNewCustomer(admin.ModelAdmin):
    list_display = ['first_name', 'last_name',  'address', 'phone', 'email', 'password']

# Register your models here.
admin.site.register(Customer)
admin.site.register(Product, AdminProduct)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
admin.site.register(NewCustomer, AdminNewCustomer)
admin.site.register(Category, AdminCategory)
admin.site.register(Seller)

