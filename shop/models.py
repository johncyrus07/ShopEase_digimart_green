import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from decimal import Decimal

uid = uuid.uuid4
class BaseUser(AbstractUser):
 id=models.UUIDField(primary_key=True,default=uid,editable=False)
 middle_name=models.CharField(max_length=100,blank=True)
 gender=models.CharField(max_length=30,blank=True)
 avatar=models.ImageField(upload_to='avatars/',blank=True,null=True)
 email=models.EmailField(unique=True)
 class Meta: db_table='base_users'
 def __str__(self): return self.username
PRODUCT_PHOTOS = {'SE-001': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=650&q=85', 'SE-002': 'https://images.unsplash.com/photo-1606220588913-b3aacb4d2f46?auto=format&fit=crop&w=650&q=85', 'SE-003': 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=650&q=85', 'SE-004': 'https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?auto=format&fit=crop&w=650&q=85', 'SE-005': 'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?auto=format&fit=crop&w=650&q=85', 'SE-006': 'https://images.unsplash.com/photo-1527814050087-3793815479db?auto=format&fit=crop&w=650&q=85', 'SE-007': 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&w=650&q=85', 'SE-008': 'https://images.unsplash.com/photo-1603891128711-11b4b03bb138?auto=format&fit=crop&w=650&q=85', 'SE-009': 'https://images.unsplash.com/photo-1609091839311-d5365f9ff1c5?auto=format&fit=crop&w=650&q=85', 'SE-010': 'https://images.unsplash.com/photo-1547949003-9792a18a2601?auto=format&fit=crop&w=650&q=85', 'SE-011': 'https://images.unsplash.com/photo-1587829741301-dc798b83add3?auto=format&fit=crop&w=650&q=85', 'SE-012': 'https://images.unsplash.com/photo-1583863788434-e58a36330cf0?auto=format&fit=crop&w=650&q=85', 'SE-013': 'https://images.unsplash.com/photo-1524592094714-0f0654e20314?auto=format&fit=crop&w=650&q=85', 'SE-014': 'https://images.unsplash.com/photo-1528825871115-3581a5387919?auto=format&fit=crop&w=650&q=85', 'SE-015': 'https://images.unsplash.com/photo-1602143407151-7111542de6e8?auto=format&fit=crop&w=650&q=85', 'SE-016': 'https://images.unsplash.com/photo-1615663245857-ac93bb7c39e7?auto=format&fit=crop&w=650&q=85'}

class Product(models.Model):
 id=models.UUIDField(primary_key=True,default=uid,editable=False)
 name=models.CharField(max_length=200)
 description=models.TextField(blank=True)
 sku=models.CharField(max_length=50,unique=True)
 price=models.DecimalField(max_digits=10,decimal_places=2,validators=[MinValueValidator(Decimal('0.00'))])
 stock=models.PositiveIntegerField(default=0)
 thumbnail=models.ImageField(upload_to='products/',blank=True,null=True)
 is_active=models.BooleanField(default=True)
 created_at=models.DateTimeField(auto_now_add=True)
 updated_at=models.DateTimeField(auto_now=True)
 class Meta: db_table='products';ordering=['-created_at']
 @property
 def storefront_photo(self):
  if self.thumbnail and not self.thumbnail.name.lower().endswith('.svg'):
   return self.thumbnail.url
  return PRODUCT_PHOTOS.get(self.sku, '')
 def __str__(self): return self.name
class Cart(models.Model):
 id=models.UUIDField(primary_key=True,default=uid,editable=False)
 owner=models.OneToOneField(BaseUser,on_delete=models.CASCADE,related_name='cart')
 created_at=models.DateTimeField(auto_now_add=True)
 updated_at=models.DateTimeField(auto_now=True)
 class Meta: db_table='carts'
 @property
 def total(self): return sum((line.subtotal for line in self.cart_products.select_related('product')),Decimal('0.00'))
class CartProduct(models.Model):
 id=models.UUIDField(primary_key=True,default=uid,editable=False)
 quantity=models.PositiveIntegerField(default=1,validators=[MinValueValidator(1)])
 cart=models.ForeignKey(Cart,on_delete=models.CASCADE,related_name='cart_products')
 product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='cart_products')
 class Meta: db_table='cart_products';constraints=[models.UniqueConstraint(fields=['cart','product'],name='unique_cart_product')]
 @property
 def subtotal(self): return self.quantity*self.product.price
class Transaction(models.Model):
 id=models.UUIDField(primary_key=True,default=uid,editable=False)
 buyer=models.ForeignKey(BaseUser,on_delete=models.PROTECT,related_name='transactions')
 created_at=models.DateTimeField(auto_now_add=True)
 class Meta: db_table='transactions';ordering=['-created_at']
 @property
 def total(self): return sum((line.subtotal for line in self.product_transactions.all()),Decimal('0.00'))
class ProductTransaction(models.Model):
 id=models.UUIDField(primary_key=True,default=uid,editable=False)
 quantity=models.PositiveIntegerField(validators=[MinValueValidator(1)])
 item=models.ForeignKey(Product,on_delete=models.PROTECT,related_name='product_transactions')
 transaction=models.ForeignKey(Transaction,on_delete=models.CASCADE,related_name='product_transactions')
 unit_price=models.DecimalField(max_digits=10,decimal_places=2,default=0)
 class Meta: db_table='product_transactions'
 @property
 def subtotal(self): return self.quantity*self.unit_price
