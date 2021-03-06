from django.shortcuts import render, redirect,get_object_or_404
from store.models import Product,Variation
from .models import Cart , CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.http import HttpResponse

def _cart_id(request):          #private Function, i.e function to fetch the cart_id from the browser
    cart = request.session.session_key      #session_key is present in the cookies
    if not cart:
        cart =request.session.create()
    return cart


def add_cart(request, product_id):
    current_user = request.user
    product = Product.objects.get(id=product_id)     #for getting the product
    # if the user is autheticated
    if current_user.is_authenticated:   
        product_variation =[]
        if request.method=='POST':
            for item in request.POST:   #loops through the color and the size and any value
                key = item  
                value = request.POST[key]   #it will loop through all the requests comes from the post
            

                try:
                    variation =Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)    #to check whether the key and value in the cart function is same as that in the Variation Model
                    product_variation.append(variation)
                except:
                    pass    

        is_cart_item_exists = CartItem.objects.filter(product=product,user=current_user).exists()
        if is_cart_item_exists:        #for displaying the cart and products together
            cart_item = CartItem.objects.filter(product=product, user=current_user)
            ex_var_list =[] # getting excisting variation list from the database
            id = []
            for item in cart_item: #checking whether the current variation is the excisting variation, if equal then we are going to increase the current variation
                excisting_variation = item.variations.all()
                ex_var_list.append(list(excisting_variation))
                id.append(item.id)
   

            if product_variation in ex_var_list:
                #increase the cart_item qunatity
                index=ex_var_list.index(product_variation)
                item_id=id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.qunatity +=1
                item.save()        #for saving the payment details inside the database
            else:
                #create new cart_iyem 
                item = CartItem.objects.create(product=product, qunatity=1,user =current_user)    
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)   #here the star will add all the product variations
                item.save()        #for saving the payment details inside the database
        else :
            cart_item = CartItem.objects.create(
                product = product,
                qunatity = 1,
                user= current_user,
            )
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()  
        return redirect('cart')

    ## if the user is not autheticated
    else:     
        product_variation =[]
        if request.method=='POST':
            for item in request.POST:   #loops through the color and the size and any value
                key = item  
                value = request.POST[key]   #it will loop through all the requests comes from the post
            

                try:
                    variation =Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)    #to check whether the key and value in the cart function is same as that in the Variation Model
                    product_variation.append(variation)
                except:
                    pass    
                    
    
        try:
            cart = Cart.objects.get(cart_id = _cart_id(request))    #get the cart using the cart_id present in the session
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id = _cart_id(request)
            )
        cart.save()    #for saving the payment details inside the database

        is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()
        if is_cart_item_exists:        #for displaying the cart and products together
            cart_item = CartItem.objects.filter(product=product, cart=cart)
            #excisting variations - From database
            # Current Variations
            # item_id - From database
            ex_var_list =[] # getting excisting variation list from the database
            id = []
            for item in cart_item: #checking whether the current variation is the excisting variation, if equal then we are going to increase the current variation
                excisting_variation = item.variations.all()
                ex_var_list.append(list(excisting_variation))
                id.append(item.id)

            print(ex_var_list)    

            if product_variation in ex_var_list:
                #increase the cart_item qunatity
                index=ex_var_list.index(product_variation)
                item_id=id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.qunatity +=1
                item.save()
            else:
                #create new cart_iyem 
                item = CartItem.objects.create(product=product, qunatity=1,cart=cart)    
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)   #here the star will add all the product variations
                item.save()
        else :
            cart_item = CartItem.objects.create(
                product = product,
                qunatity = 1,
                cart = cart,
            )
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()  
        return redirect('cart')

def remove_cart(request, product_id,cart_item_id):
 
    product = get_object_or_404(Product, id = product_id)
    try:
        if request.user.is_authenticated:
             cart_item = CartItem.objects.get(product=product,user=request.user,id=cart_item_id)
        else:
               cart = Cart.objects.get(cart_id=_cart_id(request))
               cart_item = CartItem.objects.get(product=product,cart=cart,id=cart_item_id)
        if cart_item.qunatity > 1:
            cart_item.qunatity -=1
            cart_item.save()
        else:
            cart_item.delete()
    except:
          pass       
    return redirect('cart')    


def remove_cart_item(request, product_id,cart_item_id):
       
    product = get_object_or_404(Product, id= product_id)
    if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product,user=request.user, id=cart_item_id)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request)) 
        cart_item = CartItem.objects.get(product=product,cart=cart, id=cart_item_id)
    cart_item.delete()
    return redirect('cart')
    




def cart(request,total=0, qunatity=0, cart_items=None):
    try:
        tax=0
        grand_total=0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.qunatity)
            qunatity += cart_item.qunatity
        tax = (2 * total)/100
        grand_total = total +tax
        
    except ObjectDoesNotExist:  
        pass    #just ignore      
    

    context = {                          #for passing all the values to the templates
        'total': total,
        'qunatity': qunatity,
        'cart_items': cart_items,
        'tax'       : tax,
        'grand_total': grand_total,
    }

    return render(request,'store/cart.html', context)                


@login_required(login_url='login')
def checkout(request,total=0, qunatity=0, cart_items=None):
     try:
        tax = 0
        grand_total = 0 
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.qunatity)
            qunatity += cart_item.qunatity
        tax = (2 * total)/100
        grand_total = total +tax
        
     except ObjectDoesNotExist:  
        pass    #just ignore      
    

     context ={  #for passing all the values to the templates
        'total': total,
        'qunatity': qunatity,
        'cart_items': cart_items,
        'tax'       : tax,
        'grand_total': grand_total,
    }
     return render(request, 'store/checkout.html', context)