from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
import datetime
from .models import * 
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import  check_password
from .utils import cookieCart, cartData, guestOrder

def store(request):

	data = cartData(request)
	cartItems = data['cartItems']

	products = Product.objects.all()
	context = {'products':products, 'cartItems':cartItems}
	return render(request, 'store/store.html', context)


def cart(request):

	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/cart.html', context)

def checkout(request):
	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/checkout.html', context)

def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:

		orderItem.delete()

	return JsonResponse('Item was added', safe=False)

def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
	else:
		customer, order = guestOrder(request, data)

	total = float(data['form']['total'])
	order.transaction_id = transaction_id

	if total == float(order.get_cart_total):
		order.complete = True
	order.save()

	if Order.shipping == True:
		ShippingAddress.objects.create(
		customer=customer,
		order=order,
		address=data['shipping']['address'],
		city=data['shipping']['city'],
		state=data['shipping']['state'],
		zipcode=data['shipping']['zipcode'],
		)

	return JsonResponse('Payment submitted..', safe=False)

class Signup(View):
    def get(self, request):
        return render(request, 'store/signup.html')

    def post(self, request):
        postData = request.POST
        first_name = postData.get('firstname')
        last_name = postData.get('lastname')
        address = postData.get('address')
        phone = postData.get('phone')
        email = postData.get('email')
        password = postData.get('password')
        # validation
        value = {
            'first_name': first_name,
            'last_name': last_name,
            'address': address,
            'phone': phone,
            'email': email
        }
        error_message = None

        newcustomer = NewCustomer(first_name=first_name,
                            last_name=last_name,
                            address=address,
                            phone=phone,
                            email=email,
                            password=password)
        error_message = self.validateNewCustomer(newcustomer)

        if not error_message:
            print(first_name, last_name, address, phone, email, password)
            newcustomer.password = make_password(newcustomer.password)
            newcustomer.register()
            return redirect('store')
        else:
            data = {
                'error': error_message,
                'values': value
            }
            return render(request, 'store/signup.html', data)

    def validateNewCustomer(self, newcustomer):
        error_message = None;
        if (not newcustomer.first_name):
            error_message = "First Name Required !!"
        elif len(newcustomer.first_name) < 4:
            error_message = 'First Name must be 4 char long or more'
        elif not newcustomer.last_name:
            error_message = 'Last Name Required'
        elif len(newcustomer.last_name) < 4:
            error_message = 'Last Name must be 4 char long or more'
        elif not newcustomer.address:
            error_message = 'address Required'
        elif len(newcustomer.last_name) < 4:
            error_message = 'Last Name must be 4 char long or more'    
        elif not newcustomer.phone:
            error_message = 'Phone Number required'
        elif len(newcustomer.phone) < 10:
            error_message = 'Phone Number must be 10 char Long'
        elif len(newcustomer.password) < 6:
            error_message = 'Password must be 6 char long'
        elif len(newcustomer.email) < 5:
            error_message = 'Email must be 5 char long'
        elif newcustomer.isExists():
            error_message = 'Email Address Already Registered..'
        # saving

        return error_message

class Login(View):
    return_url = None
    def get(self , request):
        Login.return_url = request.GET.get('return_url')
        return render(request , 'store/login.html')

    def post(self , request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        newcustomer = NewCustomer.get_NewCustomer_by_email(email)
        error_message = None
        if newcustomer:
            flag = check_password(password, newcustomer.password)
            if flag:
                request.session['newcustomer'] = newcustomer.id

                if Login.return_url:
                    return HttpResponseRedirect(Login.return_url)
                else:
                    Login.return_url = None
                    return redirect('store')
            else:
                error_message = 'Email or Password invalid !!'
        else:
            error_message = 'Email or Password invalid !!'

        print(email, password)
        return render(request, 'store/login.html', {'error': error_message})

def logout(request):
    request.session.clear()
    return redirect('store')        

class Signup1(View):
    def get(self, request):
        return render(request, 'store/signup1.html')

    def post(self, request):
        postData = request.POST
        first_name = postData.get('firstname')
        last_name = postData.get('lastname')
        address = postData.get('address')
        phone = postData.get('phone')
        email = postData.get('email')
        password = postData.get('password')
        # validation
        value = {
            'first_name': first_name,
            'last_name': last_name,
            'address': address,
            'phone': phone,
            'email': email
        }
        error_message = None

        seller = Seller(first_name=first_name,
                            last_name=last_name,
                            address=address,
                            phone=phone,
                            email=email,
                            password=password)
        error_message = self.validateSeller(seller)

        if not error_message:
            print(first_name, last_name, address, phone, email, password)
            seller.password = make_password(seller.password)
            seller.register()
            return redirect('store')
        else:
            data = {
                'error': error_message,
                'values': value
            }
            return render(request, 'store/signup.html', data)

    def validateSeller(self, seller):
        error_message = None;
        if (not seller.first_name):
            error_message = "First Name Required !!"
        elif len(seller.first_name) < 4:
            error_message = 'First Name must be 4 char long or more'
        elif not seller.last_name:
            error_message = 'Last Name Required'
        elif len(seller.last_name) < 4:
            error_message = 'Last Name must be 4 char long or more'
        elif not seller.address:
            error_message = 'address Required'
        elif len(seller.last_name) < 4:
            error_message = 'Last Name must be 4 char long or more'    
        elif not seller.phone:
            error_message = 'Phone Number required'
        elif len(seller.phone) < 10:
            error_message = 'Phone Number must be 10 char Long'
        elif len(seller.password) < 6:
            error_message = 'Password must be 6 char long'
        elif len(seller.email) < 5:
            error_message = 'Email must be 5 char long'
        elif seller.isExists():
            error_message = 'Email Address Already Registered..'
        # saving

        return error_message

class Login1(View):
    return_url = None
    def get(self , request):
        Login1.return_url = request.GET.get('return_url')
        return render(request , 'store/login1.html')

    def post(self , request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        seller = Seller.get_Seller_by_email(email)
        error_message = None
        if seller:
            flag = check_password(password, seller.password)
            if flag:
                request.session['seller'] = seller.id

                if Login1.return_url:
                    return HttpResponseRedirect(Login1.return_url)
                else:
                    Login1.return_url = None
                    return redirect('store')
            else:
                error_message = 'Email or Password invalid !!'
        else:
            error_message = 'Email or Password invalid !!'

        print(email, password)
        return render(request, 'store/login1.html', {'error': error_message})

def Edit_profile(request):
    context = {}
    data = NewCustomer.objects.filter(email=NewCustomer.email)
    context["data"]=data
    return render(request, 'store/edit_profile.html',context)





        



						  				
