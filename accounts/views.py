from django.forms.models import inlineformset_factory
from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from .models import *
from .forms import OrderForm, CreateUserForm, CustomerForm
from .filters import OrderFilter
from .decorators import unauthenticated_user, allowed_users, admin_only

# Main Page / Dashboard with all important data
@login_required(login_url='login')
@admin_only
def dashboard(request):
	orders = Order.objects.all().order_by('-id')
	customers = Customer.objects.all()

	total_customers = customers.count()
	total_orders = orders.count()

	delivered = orders.filter(status='تحویل داده شده').count()
	pending = orders.filter(status='در حال بررسی').count()
	out_for_delivery = orders.filter(status='سفارشات در مسیر تحویل').count()

	context = {
		'orders': orders,
		'customers': customers,
		'total_customers': total_customers,
		'total_orders': total_orders,
		'delivered': delivered,
		'pending': pending,
		'out_for_delivery': out_for_delivery,
	}

	return render(request, 'accounts/dashboard.html', context=context)


# User Profile Page
@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
	orders = request.user.customer.order_set.all()
	total_orders = orders.count()

	delivered = orders.filter(status='تحویل داده شده').count()
	pending = orders.filter(status='در حال بررسی').count()
	out_for_delivery = orders.filter(status='سفارشات در مسیر تحویل').count()

	context = {
		'orders': orders,
		'total_orders': total_orders,
		'delivered': delivered,
		'pending': pending,
		'out_for_delivery': out_for_delivery,
	}
	return render(request, 'accounts/user.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
	customer = request.user.customer
	form = CustomerForm(instance=customer)

	if request.method == 'POST':
		form = CustomerForm(request.POST, request.FILES, instance=customer)
		if form.is_valid():
			form.save()
			messages.success(request, 'اطلاعات %s با موفقیت تغییر یافت!' % form.cleaned_data.get('name'))
			redirect('account')


	context = {
		'form': form,
	}
	return render(request, 'accounts/account_settings.html', context)


@unauthenticated_user
def loginPage(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect('dashboard')
		else:
			messages.info(request, 'نام کاربری یا کلمه عبور اشتباه است')

	context = {}
	return render(request, 'accounts/login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('dashboard')

@unauthenticated_user
def registerPage(request):
	form = CreateUserForm()
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			messages.success(request, 'اکانت برای ' + form.cleaned_data.get('username') + ' ساخته شد')
			return redirect('login')

	context = {
		'form': form,
	}
	return render(request, 'accounts/register.html', context)


# Products.html View with list of all products
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
	products = Product.objects.all()
	return render(request, 'accounts/products.html', context={'products': products})


# Each Customer has the unique page with this view
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request, pk):
	customer = Customer.objects.get(id=pk)

	orders = customer.order_set.all()
	order_count = orders.count()

	myFilter = OrderFilter(request.GET, queryset=orders)
	orders = myFilter.qs

	context = {
		'customer': customer,
		'orders': orders,
		'order_count': order_count,
		'myFilter': myFilter,
	}
	return render(request, 'accounts/customer.html', context=context)


# Create New Order Form
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createOrder(request, pk):
	OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=2)
	customer = Customer.objects.get(id=pk)
	formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
	# form = OrderForm(initial={'customer': customer})

	if request.method == 'POST':
		# form = OrderForm(request.POST)
		formset = OrderFormSet(request.POST, instance=customer)
		if formset.is_valid():
			formset.save()
			return redirect('/')

	context = {'formset': formset}
	return render(request, 'accounts/order_form.html', context)


# Update and Change Current Order Form
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request, pk):

	order = Order.objects.get(id=pk)
	formset = OrderForm(instance=order)

	if request.method == 'POST':
		formset = OrderForm(request.POST, instance=order)
		if formset.is_valid():
			formset.save()
			return redirect('/')

	context = {'formset': formset}
	return render(request, 'accounts/update_order.html', context)


# Delete an Existing Order Form
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request, pk):
	order = Order.objects.get(id=pk)
	if request.method == 'POST':
		order.delete()
		return redirect('/')

	context = {'item': order}
	return render(request, 'accounts/delete.html', context)