from django.contrib.auth.models import User
from django.db import models
from cart.models import Dataset, DownloadLink
# Create your models here.
class Profile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    image= models.ImageField(default="default.jpg",upload_to="profile_pictures")
    first_name = models.CharField(max_length=50,default=" ")
    last_name = models.CharField(max_length=50,default=" ")
    address = models.CharField(max_length=100,default=" ")
    phone_number = models.CharField(max_length=15,default=" ")
    class Meta:
        app_label = 'users'
    def __str__(self):
        return f"{self.user.username} Profile"


class PurchasedItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)
    download_link = models.ForeignKey(DownloadLink, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} - {self.dataset.name}'