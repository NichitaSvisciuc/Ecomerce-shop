from django.contrib import admin

from .models import *

class OrderAdmin(admin.ModelAdmin):

	list_filter = ['ordered']

	search_fields = [
		'user__username',
	]

admin.site.register(Clothe)
admin.site.register(DiscountCodes)
admin.site.register(Order, OrderAdmin)
admin.site.register(Stash)
admin.site.register(OrderItem)