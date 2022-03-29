from django.shortcuts import render, get_object_or_404,redirect
from .models import Product,ReviewRating
from category.models import Category
from carts.models import CartItem
from django.db.models import Q
from orders.models import OrderProduct

from carts.views import _cart_id
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse
from.forms import ReviewForm
from django.contrib import messages

# Create your views here.
def store(request, category_slug=None):
    categories = None
    products   = None

    if category_slug != None:
        categories = get_object_or_404(Category ,slug = category_slug)
        products   = Product.objects.filter(category=categories, is_available=True)
        paginator = Paginator(products, 1)  # paginator = Paginator(products, 6)=No. of products that is shown in one page
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)       #the 6 products is get stored in the paged_products
        product_count = products.count()
    else:

        products = Product.objects.all().filter(is_available=True).order_by('id')
        paginator = Paginator(products, 3)  # paginator = Paginator(products, 6)=No. of products that is shown in one page
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)       #the 6 products is get stored in the paged_products
        product_count = products.count()

    context={
        'products':   paged_products,
         'product_count' : products.count,
    }
    return render(request,'store/store.html',context)

def product_detail(request,category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)        #to get access to a specific product
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()        #cart__cart_id= To acccess the cart_id using the cart(as cart is a foreign key)

    except Exception as e:
         raise e

    #to check whether the user has purchase the proudct and only if he had purchased the prodcut he can add the reviews
    try:
        orderproduct =   OrderProduct.objects.filter(user=request.user,product_id=single_product.id).exists()

    except OrderProduct.DoesNotExist:
        orderproduct = None


    #get the reviews  
    reviews = ReviewRating.objects.filter(product_id=single_product.id, status=True)  

    context = {
        'single_product':single_product,
        'in_cart'       :in_cart,
        'orderproduct'  :orderproduct, 
        'reviews' : reviews,
        
    }

    return render(request,'store/product_detail.html',context)



def search(request):
     if 'keyword' in request.GET:       #checking whether the GET request has the keyword or not
         keyword = request.GET['keyword']
         if keyword:
             products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword ) | (Q(product_name__icontains=keyword)))    #description__icontains=keyword-it checks whether the keyword is in the description and if keyword is there it will bring the results in the search result page
             product_count = products.count()            #Q = OR operation
 
     context = {                                       
         'products' : products,
         'product_count' : product_count,           

     }  
     return render(request,'store/store.html',context)

def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')      #for storing the previous Url,i.e to redirect back to the current page
    if request.method=='POST':
        try:
            reviews=ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
            form = ReviewForm(request.POST,instance=reviews)     #here we are having all the data of the starts, reviews and ratings
            form.save()                                               #instance=reviews=For updating the excisting review 
            messages.success(request,'Thank you! Your review has been updated')
            return redirect(url)            # to redirect back to the current page
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST) 
            if form.is_valid():
                data =  ReviewRating()
                data.subject=form.cleaned_data['subject']    
                data.rating=form.cleaned_data['rating'] 
                data.review=form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')      #REMOTE__ADDR= For storing the ip address
                data.product_id = product_id
                data.user_id=request.user.id
                data.save()   
                messages.success(request,'Thank you! Your review has been submiited')    
                return redirect(url)                                    