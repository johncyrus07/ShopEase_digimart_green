from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import BaseUser,Product,Cart,CartProduct,Transaction,ProductTransaction
@admin.register(BaseUser)
class BaseUserAdmin(UserAdmin):
 fieldsets=UserAdmin.fieldsets+(('Additional information',{'fields':('middle_name','gender','avatar')}),)
 add_fieldsets=UserAdmin.add_fieldsets+(('Email',{'fields':('email',)}),)
 list_display=('username','email','is_staff','is_active')
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
 list_display=('name','sku','price','stock','is_active')
 search_fields=('name','sku')
 list_filter=('is_active',)
class CartProductInline(admin.TabularInline):
 model=CartProduct;extra=0
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
 list_display=('owner','created_at');inlines=[CartProductInline]
class ProductTransactionInline(admin.TabularInline):
 model=ProductTransaction;extra=0;readonly_fields=('item','quantity','unit_price');can_delete=False
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
 list_display=('id','buyer','created_at','total');inlines=[ProductTransactionInline]
 def has_add_permission(self,request): return False
admin.site.register(CartProduct)
admin.site.register(ProductTransaction)

admin.site.site_header='ShopEase Administration'
admin.site.site_title='ShopEase Admin'
admin.site.index_title='ShopEase Store Management'
