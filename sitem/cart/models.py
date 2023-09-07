from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    items = models.ManyToManyField('Dataset', through='CartItem')

    @property
    def purchased(self):
        return self.items

class Dataset(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='datasets/')
    price = models.DecimalField(max_digits=10, decimal_places=2)


# Update CartItem to reference Dataset
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE,default=None, null=True)
    quantity = models.PositiveIntegerField(default=1)
    download_token = models.CharField(max_length=50, null=True, blank=True)
    link_expiration = models.DateTimeField(null=True, blank=True)
    checked_out=models.BooleanField(default=False)


class DownloadLink(models.Model):
    download_token = models.CharField(max_length=100, unique=True)
    link_expiration = models.DateTimeField()
    def __str__(self):
        return self.download_token

