from django.contrib import admin
from .models import listing, price, comment

# Register your models here.
admin.site.register(listing)
admin.site.register(price)
admin.site.register(comment)