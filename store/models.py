from django.db import models
from category.models import Category
from django.urls import reverse
from accounts.models import Account
from django.db.models import Avg, Count

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

    def  averageReview(self):
        reviews=ReviewRating.objects.filter(product=self, status=True).aggregate(average=Avg('rating'))
        avg=0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg      

    def countReview(self):
         reviews=ReviewRating.objects.filter(product=self, status=True).aggregate(count=Count('id'))
         count=0
         if reviews['count'] is not None:
            count = int(reviews['count'])
         return count

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


class ReviewRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)     #CASCADE is beacause if the product is deleted then the review ratings should be deleted
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, blank =True)
    review = models.TextField(max_length=500, blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)  #the status field is bcz if the admin want to delete the rating, he can delete it 
    created_date = models.DateTimeField(auto_now_add=True)    
    updated_at= models.DateTimeField(auto_now=True)


    def __str__(self):                                          #string represenatation of the Model
        return self. subject

class ProductGallery(models.Model):
    product = models.ForeignKey(Product,default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='store/products/',max_length=255)


    def __str__(self):
        return self.product.product_name

    class Meta:     #This class is created because django autimatcially add an 's' to every models to make it plural, so for removing that 's' we are using this class
        verbose_name = 'productgallery'
        verbose_name_plural = 'product gallery'    


