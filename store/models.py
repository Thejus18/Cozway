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

class VariationManager(models.Manager):     #to manage the querys
        def colors(self):
            return super (VariationManager,self).filter(variation_category='color', is_active=True)

        def sizes(self):
            return super(VariationManager,self).filter(variation_category='size',is_active=True)    

variation_category_choice=(
    ('color', 'color'),
    ('size', 'size')
)

class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE) #bcz we are going to add the variation of the product and therefore we need this product as the foreign key
    variation_category=models.CharField(max_length=100, choices=variation_category_choice)                      #CASCADE is beacause if the product is deleted then the variation should be deleted
    variation_value = models.CharField(max_length=100)
    is_active    = models.BooleanField(default=True)    #to disable any variation field
    created_date = models.DateTimeField(auto_now=True)

    objects = VariationManager()

    def __str__(self):
        return self. variation_value