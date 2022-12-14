from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    watchlist = models.ManyToManyField('Auction', blank=True)

class Category(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name}"
    
class Auction(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seller')
    title = models.CharField(max_length=64)
    description = models.TextField()
    starting_bid = models.FloatField()
    imageURL = models.URLField()
    category = models.ManyToManyField(Category, blank=True)
    winner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    has_winner = models.BooleanField(default=False)
    

    def max_bid(self):
        if Bid.objects.filter(item=self):
            max_bid = max(list(bid.bid for bid in Bid.objects.filter(item=self)))
            return max_bid
        return 0

    def count_bid(self):
        count_bid = len(list(bid.bid for bid in Bid.objects.filter(item=self)))
        return count_bid

    def __str__(self):
        return f"{self.title}"

class Bid(models.Model):
    item = models.ForeignKey(Auction, on_delete=models.CASCADE)
    purchaser = models.ForeignKey(User, on_delete=models.CASCADE)
    bid = models.FloatField()

class Comment(models.Model):
    item = models.ForeignKey(Auction, on_delete=models.CASCADE)
    purchaser = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.CharField(max_length=64, blank=True)
    description = models.TextField()