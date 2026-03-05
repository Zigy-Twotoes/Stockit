from django.db import models
from django.conf import settings

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=100)
    par = models.IntegerField(default=0)

class OrderGuide(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    products = models.ManyToManyField(Product, through='OrderList')

class OrderList(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    guide = models.ForeignKey(OrderGuide, on_delete=models.CASCADE)
    stock_on_hand = models.IntegerField(default=0)
    quantity_ordered = models.IntegerField(default=0)
    par_level = models.IntegerField(null=True, blank=True)
    order_date = models.DateField(auto_now_add=True)
    def save(self, *args, **kwargs):
        if not self.par_level:
            self.par_level = self.product.par
        self.quantity_ordered = max(0, self.par_level - self.stock_on_hand)
        super().save(*args, **kwargs)
    @property
    def suggested_order(self):
        return max(0 self.par_level - self.stock_on_hand)