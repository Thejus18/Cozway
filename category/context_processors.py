from .models import Category

def menu_links(request):    #going to fetch all the cateogories from the database
   links = Category.objects.all()
   return dict(links=links)    

