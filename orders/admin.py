from django.contrib import admin
from.models import Payment, Order, OrderProduct

# Register your models here.

#tabular Inline-- 
class OrderProductInline(admin.TabularInline):      #to apend the orderProduct table below the orders
    model=OrderProduct
    readonly_fields = ('payment', 'user', 'product', 'qunatity', 'product_price', 'ordered')
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number','full_name','phone','email','city','order_total','tax','status','ip','is_ordered','created_at']
    list_filter= ['status', 'is_ordered']
    search_fileds = ['order_number','first_name','last_name','phone','email']
    list_per_page =20
    inlines = [OrderProductInline]      #to apend the orderProduct table below the orders




admin.site.register(Payment)
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderProduct)