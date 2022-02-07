from django.contrib import admin
from .models import User, listing, price, comment

# Register your models here.
admin.site.register(listing)
admin.site.register(price)
admin.site.register(comment)
admin.site.register(User)