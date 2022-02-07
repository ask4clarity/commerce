from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
	pass
	
class listing(models.Model):
	CATEGORIES = (
		('AN', 'Antiques'), 
		('AR', 'Art'),
		('BO', 'Books'),
		('CL', 'Clothing'),
		('FI', 'Film'),
		('MU', 'Music'),
		('GA', 'Games'),
)

	title = models.CharField(max_length=80)
	description = models.TextField()
	image = models.ImageField(upload_to='images/', blank=True)
	date = models.DateTimeField(auto_now_add=True)
	starting_price = models.DecimalField(max_digits=10, decimal_places=2)
	closed = models.BooleanField(default=False)
	category = models.CharField(max_length=2, choices=CATEGORIES)
	owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="creator")
	winner = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="top", null=True, default=None)
	watching = models.ManyToManyField(User, related_name="watchlist")
	
	def __str__(self):
		return f"{self.title}"

class price(models.Model):
	item = models.ForeignKey(listing, on_delete=models.CASCADE, related_name="items")
	bidder = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name="purchaser")
	bid = models.DecimalField(max_digits=10, decimal_places=2, null=True)
	
	def __str__(self):
		return f"{self.item} bid: {self.bid}"

class comment(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commenter")
	for_sale = models.ForeignKey(listing, on_delete=models.CASCADE, related_name="opinions")
	comments = models.TextField()