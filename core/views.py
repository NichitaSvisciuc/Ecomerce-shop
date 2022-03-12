from django.shortcuts import render, redirect

from django.views.generic.list import ListView
from django.views.generic import DetailView, View

from django.core.paginator import Paginator, EmptyPage

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.http import HttpResponse

from django.db.models.signals import post_save
from django.dispatch import receiver

from django.db.models import Q

from .models import *
from .forms import *

import datetime


class ItemDetailView(DetailView):

	model = Clothe
	template_name = 'single-product.html'
	
@login_required
def checkout(request):
	
	stash = Stash.objects.get(user = request.user)

	context = {
		'stash' : stash,

	}		

	return render(request, 'checkout.html', context)

@login_required
def order(request):

	name = request.POST.get('name')
	email = request.POST.get('email')
	number = request.POST.get('number')
	code = request.POST.get('code')
	country = request.POST.get('country')
	discount_code = request.POST.get('discount_code')

	stash = Stash.objects.get(user = request.user)
	items = Clothe.objects.all()

	order = Order.objects.create(
		user = request.user,
		name = name,
		email = email,
		number = number,
		code = code,
		country = country,
		total_price = stash.get_total_price(),
		date = datetime.datetime.now(),
		ordered = False,
	)

	# Finding and calculating the discount code
	total_price = stash.get_total_price()
	dicount_codes = DiscountCodes.objects.all()

	for code in dicount_codes:
		if discount_code == code.code_body:

			discount = DiscountCodes.objects.get(code_body = discount_code)

			if discount.uses > 1:

				discount.uses -= 1
				discount.save()
			else:
				
				discount.delete()	

			order.total_price = total_price - ((total_price * discount.discount_percentage) / 100)
			order.save()
	# ---------------------------------------- #		

	items_stash = stash.items.all()
	item = []

	for i in items_stash:
		item.append(str(i))

	order.items = item

	order.save()

	items_stash.delete()

	stash.items.clear()

	return redirect('home')	

@login_required
def products(request):

	stash = Stash.objects.get(user = request.user)

	orders = Order.objects.filter(user = request.user)

	context = {
		'stash' : stash,
		'orders' : orders,
	}

	return render(request, 'products.html', context)	

def home(request):

	search = request.GET.get('search', '')

	if search:
		clothes = Clothe.objects.filter(Q(name__icontains = search) | Q(price__icontains = search))
	else:
		clothes = Clothe.objects.all()

	pagins = Paginator(clothes, 2)

	number_of_pages = pagins.num_pages

	page_taken = request.GET.get('page', 1)

	try:
		page = pagins.page(page_taken)
	except EmptyPage:
		page = pagins.page(1)		

	context = {
		'clothes' : page,
		'number_of_pages' : number_of_pages,
	}	

	return render(request, 'index.html', context)

@login_required
def add_to_cart(request):

	item_id = request.GET.get('clothe_id')
	quantity = int(request.GET.get('quantity'))

	item = Clothe.objects.get(id = item_id)
	stash = Stash.objects.get(user = request.user)

	if item.in_stock >= quantity:

		order_item, created = OrderItem.objects.get_or_create(item = item, user = request.user)

		if created:

			order_item.quantity = quantity
			order_item.save()

			stash.items.add(order_item)
			stash.save()
		else:
			
			order_item.quantity += int(quantity)
			order_item.save()	

	else:
		
		print("not enough items")		

	return redirect('item', slug = item.slug)

@login_required
def remove_from_cart(request, id):

	item = OrderItem.objects.get(id = id)
	item.delete()

	return redirect('products')

@login_required
def add_single_item(request, id):
	
	item = OrderItem.objects.get(id = id)
	item.quantity += 1

	item.save()

	return redirect('products')

@login_required
def remove_single_item(request, id):
	
	item = OrderItem.objects.get(id = id)
	item.quantity -= 1	

	item.save()	

	if item.quantity == 0:

		item.delete()

	return redirect('products')	

def register(request):

	if request.method == 'POST':
		form = UserRegisterForm(request.POST)

		if form.is_valid():

			form.save()	

			return redirect('login')
	else:
		form = UserRegisterForm()
	

	return render(request, 'reg.html', {'form': form})	

@receiver(post_save, sender = User)
def create_user_picks(sender, instance, created, **kwargs):

	if created:
		Stash.objects.create(user = instance)