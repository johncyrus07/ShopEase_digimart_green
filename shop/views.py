from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.db import transaction as db_transaction
from django.db.models import F
from .models import Product,Cart,CartProduct,Transaction,ProductTransaction
from .forms import RegisterForm

def home(request):
 products=Product.objects.filter(is_active=True)
 q=request.GET.get('q','').strip()
 if q: products=products.filter(name__icontains=q)
 return render(request,'shop/home.html',{'products':products,'q':q})
def detail(request,pk): return render(request,'shop/detail.html',{'product':get_object_or_404(Product,pk=pk,is_active=True)})
def register(request):
 form=RegisterForm(request.POST or None)
 if request.method=='POST' and form.is_valid():
  user=form.save();login(request,user);messages.success(request,'Account created!');return redirect('home')
 return render(request,'shop/register.html',{'form':form})
@login_required
def cart(request):
 c,_=Cart.objects.get_or_create(owner=request.user)
 return render(request,'shop/cart.html',{'cart':c,'lines':c.cart_products.select_related('product')})
@login_required
@require_POST
def add_to_cart(request,pk):
 product=get_object_or_404(Product,pk=pk,is_active=True)
 try: qty=int(request.POST.get('quantity',1))
 except (ValueError,TypeError): qty=0
 if qty<1: messages.error(request,'Invalid quantity.');return redirect('detail',pk=pk)
 c,_=Cart.objects.get_or_create(owner=request.user)
 line,_=CartProduct.objects.get_or_create(cart=c,product=product,defaults={'quantity':0})
 if line.quantity+qty>product.stock: messages.error(request,'Not enough stock.');return redirect('detail',pk=pk)
 line.quantity+=qty;line.save();messages.success(request,'Added to cart!');return redirect('cart')
@login_required
@require_POST
def update_cart(request,pk):
 c,_=Cart.objects.get_or_create(owner=request.user)
 line=get_object_or_404(CartProduct,pk=pk,cart=c)
 try: qty=int(request.POST.get('quantity',1))
 except (ValueError,TypeError): qty=-1
 if qty==0: line.delete()
 elif 0<qty<=line.product.stock: line.quantity=qty;line.save()
 else: messages.error(request,'Invalid quantity or insufficient stock.')
 return redirect('cart')
@login_required
@require_POST
def checkout(request):
 with db_transaction.atomic():
  c,_=Cart.objects.get_or_create(owner=request.user)
  lines=list(CartProduct.objects.filter(cart=c).select_related('product'))
  if not lines: messages.error(request,'Your cart is empty.');return redirect('cart')
  products={p.pk:p for p in Product.objects.select_for_update().filter(pk__in=[l.product_id for l in lines])}
  for line in lines:
   product=products[line.product_id]
   if not product.is_active or product.stock<line.quantity:
    messages.error(request,f'Not enough stock for {product.name}.');return redirect('cart')
  order=Transaction.objects.create(buyer=request.user)
  for line in lines:
   product=products[line.product_id]
   ProductTransaction.objects.create(transaction=order,item=product,quantity=line.quantity,unit_price=product.price)
   Product.objects.filter(pk=product.pk).update(stock=F('stock')-line.quantity)
  CartProduct.objects.filter(cart=c).delete()
 messages.success(request,'Order placed successfully!');return redirect('orders')
@login_required
def orders(request):
 return render(request,'shop/orders.html',{'orders':Transaction.objects.filter(buyer=request.user).prefetch_related('product_transactions__item')})
