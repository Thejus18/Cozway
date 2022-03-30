from django.shortcuts import render,redirect
from .forms import RegistertionForm
from .models import Account
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from orders.models import Order

# Create your views here.
#verifcation Email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

from carts.views import _cart_id
from carts.models import Cart,CartItem
import requests


def register(request):
    if request.method == 'POST':
          form =  RegistertionForm(request.POST)
          if form.is_valid():
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                phone_number = form.cleaned_data['phone_number']
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']
                username = email.split("@")[0] #here we are not taking the user name from the user , instead we are giving them the user name by taking the first part of their email address(i.e before @) 
                user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
                user.phone_number = phone_number
                user.save()

                #user Activation
                current_site = get_current_site(request)
                mail_subject = 'Please activate your account'
                message = render_to_string('accounts/account_verification_email.html',{
                    'user': user,
                    'domain' : current_site,
                    'uid' : urlsafe_base64_encode(force_bytes(user.pk)),     #encoding the user_id with  urlsafe_base64_encode so that nobody can see the primary key
                    'token' : default_token_generator.make_token(user),
                })
                to_email = email
                send_email = EmailMessage(mail_subject,message,to=[to_email])
                send_email.send()
                #messages.success(request,'Thank you for registering with us . We have sent you a verification email to your email address. Please verify it.')
                return redirect('/accounts/login/?command=verification&email='+email)
    else:            
         form = RegistertionForm()
    context={               #here, we can get the context in the register.html page
        'form':form,
    }
    return render(request, 'accounts/register.html',context)
def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)


        if user is not None:
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))     
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    cart_item =CartItem.objects.filter(cart=cart)   #this will bring all the cart_items that are assigned to this cart_id
                    
                    #Getting the product variation by cart_id
                    product_variation=[]
                    for item in cart_item:
                        variation =item.variations.all()
                        product_variation.append(list(variation))  #bcz by default it's a query set

                    #get the cart items from the user to access his product variation
                    cart_item = CartItem.objects.filter( user=user)     #Here the user is the authenticated user
                    ex_var_list =[] # getting excisting variation list from the database
                    id = []
                    for item in cart_item: #checking whether the current variation is the excisting variation, if equal then we are going to increase the current variation
                        excisting_variation = item.variations.all()
                        ex_var_list.append(list(excisting_variation))
                        id.append(item.id)

                    #product_variation= [1,2,3,4,5,6]
                    #ex_var_list = [4,6,3,5]
                    #To get the common product variation inside both the above list i.e Product_variation and ex_var_list
                    for pr in product_variation:
                        if pr in ex_var_list:
                            index = ex_var_list.index(pr)   #Gives the position where the found the common item
                            item_id = id[index]
                            item = CartItem.objects.get( id=item_id)
                            item.qunatity +=1
                            item.user = user    #Assigning the current user to the cart item
                            item.save()
                        else:
                             cart_item = CartItem.objetcs.filter(cart=cart)
                             for item in cart_item:
                                item.user = user
                                item.save() 
                                
            
            except:
                pass    #it will go to the except block if only there is cart_items in the cart
            auth.login(request, user)
            messages.success(request,"You are now logged in ")
            url = request.META.get('HTTP_REFERER')  #HTTP_REFERER- it will grab the previous url from we came
            try:
                query = requests.utils.urlparse(url).query
                
                #splitting the equals part
                # next-/cart/checkout/  Here 'next' is the key and 'cart/checkout is the value
                params = dict(x.split('=') for x in query.split('&'))   # this will make- next-/cart/checkout/, the dictonary 
                if 'next' in params:
                    nextPage = params['next']
                    return redirect(nextPage)
               
            except:
                 return redirect('dashboard')
               
        else:
            messages.error(request, "Invalid login credentials")
            return redirect('login')    
    return render(request, 'accounts/login.html')



@login_required(login_url ='login')      
def logout(request):
    auth.logout(request)
    messages.success(request, 'You are logged out')
    return redirect('login')      


def activate(request,uidb64, token): #here we will decode the token and Uid
   try:
       uid = urlsafe_base64_decode(uidb64).decode()   #this will give us the primary key of the user
       user = Account._default_manager.get(pk=uid)
   except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

   if user is not None and  default_token_generator.check_token(user,token):
        user.is_active = True       
        user.save()
        messages.success(request,'Congralations!! Your account is activated')
        return redirect('login')
   else:
        messages.error(request,'Invalid activation link')
        return redirect('register')    


@login_required(login_url ='login')     #it can be acceses only if we are logged in
def dashboard(request):
    orders = Order.objects.order_by('-created_at').filter(user_id=request.user.id,is_ordered=True)
    orders_count = orders.count()
    context={
        'orders_count': orders_count,
    }
    return render(request,'accounts/dashboard.html',context)


def forgotPassword(request):
    if request.method== 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)

            #Reset password email
            current_site = get_current_site(request)
            mail_subject = 'Reset Your Password'
            message = render_to_string('accounts/reset_password_email.html',{
                    'user': user,
                    'domain' : current_site,
                    'uid' : urlsafe_base64_encode(force_bytes(user.pk)),     #encoding the user_id with  urlsafe_base64_encode so that nobody can see the primary key
                    'token' : default_token_generator.make_token(user),
                })
            to_email = email
            send_email = EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()

            messages.success(request, 'Password reset email has been sent to your email address')
            return redirect('login')

        else:
             messages.error(request, 'Account does not exist!!')
             return redirect('forgotPassword')   
    return render(request, 'accounts/forgotPassword.html')


def resetpassword_validate(request, uidb64,token):
    try:
       uid = urlsafe_base64_decode(uidb64).decode()   #this will give us the primary key of the user
       user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
        
    if user is not None and  default_token_generator.check_token(user,token):
         request.session['uid']=uid
         messages.success(request,'Please reset your password')
         return redirect('resetPassword')

    else:
         messages.error(request,'This link is actually expired')
         return redirect('login') 



def resetPassword(request):
    if request.method=='POST':
        password =request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password ==confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password) #here it will take the password and save it in the hash format
            user.save()
            messages.success(request,'Password reset succesfully')
            return redirect('login')
        else:
             messages.error(request, 'Password do not match')
             return redirect('resetPassword')  
    else:          
      return render(request,'accounts/resetPassword.html')

def my_orders(request):
    orders= Order.objects.filter(user=request.user, is_ordered=True).order_by('-created_at')    #-created_at - By putting this hypen it will give the result in descending order
    context={
        'orders': orders,
    }
    return render(request, 'accounts/my_orders.html',context)