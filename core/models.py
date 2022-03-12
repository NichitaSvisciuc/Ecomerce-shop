from django.db import models

from django.contrib.auth.models import User

from django.shortcuts import redirect
from django.shortcuts import reverse

import PIL

class Clothe(models.Model):

	class Types(models.TextChoices):
		undefined = 'Undefined Type'

		shirt = "Shirt"
		pants = "Pants"
		shoes = "Shoes"

	class Sizes(models.TextChoices):
		undefined = 'Undefined Size'

		L = "Large"
		S = "Small"

		XL = "ExtraLarge"	
		XS = "ExtraSmall"	

	category_type = models.CharField(
		max_length = 200,
		choices = Types.choices,
		default = Types.undefined
	)

	size = models.CharField(
		max_length = 200,
		choices = Sizes.choices,
		default = Sizes.undefined
	)

	name = models.CharField(max_length = 200)
	price = models.IntegerField(default = 0)
	slug = models.SlugField()

	description = models.TextField()
	image = models.ImageField(upload_to = 'media', null = True, blank = True)

	in_stock = models.IntegerField(default = 0)

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse("item", kwargs = {
			'slug' : self.slug
		})	 	

class Order(models.Model):

	user = models.ForeignKey(User, on_delete = models.CASCADE, blank = True, null = True)	

	items = models.TextField(null = True, blank = True)

	name = models.CharField(max_length = 100, null = True, blank = True)
	email = models.CharField(max_length = 100, null = True, blank = True)
	number = models.CharField(max_length = 100, null = True, blank = True)
	code = models.CharField(max_length = 100, null = True, blank = True)
	country = models.CharField(max_length = 100, null = True, blank = True)

	date = models.DateTimeField()
	total_price = models.IntegerField()

	ordered = models.BooleanField(default = False)

	def __str__(self):
		return self.user.username

class OrderItem(models.Model):

	user = models.ForeignKey(User, on_delete = models.CASCADE, blank = True, null = True)	
	
	item = models.ForeignKey(Clothe, on_delete = models.CASCADE, blank = True, null = True)	
	quantity = models.IntegerField(default = 0)

	def __str__(self):
		return f"{self.quantity} of {self.item.name}"	

	def get_remove_url(self):
		return reverse("remove_from_cart", kwargs = {
			'id' : self.id
		})	

	def add_single_item(self):
		return reverse("add_single_item", kwargs = {
			'id' : self.id
		})	

	def remove_single_item(self):
		return reverse("remove_single_item", kwargs = {
			'id' : self.id
		})	

	def get_items_total_price(self):
		return self.quantity * self.item.price

class DiscountCodes(models.Model):

	code_body = models.CharField(max_length = 50)
	discount_percentage = models.IntegerField(default = 1)

	uses = models.IntegerField(default = 1)

	def __str__(self):
		return f"{self.code_body} with {self.discount_percentage} % of discout"

class Stash(models.Model):

	user = models.ForeignKey(User, on_delete = models.CASCADE, blank = True, null = True)	

	items = models.ManyToManyField(OrderItem)

	def __str__(self):
		return self.user.username	

	def get_total_price(self):
		
		total = 0

		for i in self.items.all():
			total += i.get_items_total_price()

		return total		