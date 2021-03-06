from django.db import models
from store.models import Product,Variation
from accounts.models import Account

# Create your models here.
class Cart(models.Model):

    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add=True) 

    def __str__(self):  #to overide the objects namd of the class
       return self.cart_id


class  CartItem(models.Model):
     user = models.ForeignKey(Account, on_delete=models.CASCADE,null=True)     #i,e if the user account is deleted this cart item is also be deleted
     product = models.ForeignKey(Product, on_delete=models.CASCADE)  #ON DELETE CASCADE = specify whether you want rows deleted in a child table when corresponding rows are deleted in the parent table.
     variations = models.ManyToManyField(Variation,blank=True)
     cart    = models.ForeignKey(Cart, on_delete=models.CASCADE,null=True)
     qunatity = models.IntegerField()
     is_active = models.BooleanField(default=True)

     def sub_total(self):
        return self.product.price * self.qunatity

     def __unicode__(self):
        return self.product