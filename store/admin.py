from django.contrib import admin
from .models import Product, Variation,ReviewRating,ProductGallery
import admin_thumbnails

@admin_thumbnails.thumbnail('image') #For using the admin_thumbnail
# Register your models here.

class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery
    extra = 1

class productAdmin(admin.ModelAdmin):
    
    prepopulated_fields = {'slug' : ('product_name',)}     #for prepoplating slug
    list_display = ('product_name', 'price','stock','category','modified_date','is_available')
    inlines=[ProductGalleryInline]

class VariationAdmins(admin.ModelAdmin):
    list_display =('product','variation_category','variation_value','is_active' )
    list_editable =('is_active',)
    list_filter = ('product','variation_category','variation_value'  )


admin.site.register(Product, productAdmin)
admin.site.register(Variation,VariationAdmins )
admin.site.register(ReviewRating)
admin.site.register(ProductGallery)