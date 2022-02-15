from django.db import models
from category.models import Category
from django.urls import reverse

# Create your models here.
class Product(models.Model):
    product_name = models.CharField(max_length=200,unique=True)
    slug         = models.SlugField(max_length=255,unique=True)
    description  =  models.TextField(max_length=500,blank=True)
    price        = models.IntegerField()
    images       = models.ImageField(upload_to='photos/products')
    stock        = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category     = models.ForeignKey(Category, on_delete=models.CASCADE) #When we delete the category the product attacted to that cateogory will also be deleted
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date =models.DateTimeField(auto_now =True)


    def get_url(self):                          #this function is used to get the full details of the single product
        return reverse('product_detail', args=[self.category.slug, self.slug])     #self.slug = products slug

    def __str__(self):          #here we are using self because we are creating the function inside the model Category
         return self.product_name
