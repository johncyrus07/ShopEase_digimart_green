# ShopEase — Django E-Commerce Demo

Shopee-inspired orange-and-white storefront (independent ShopEase branding), with product search, categories, cart, checkout, account authentication, order history and Django admin. **No real payments.**

## Windows setup (Python 3.12 or 3.13 recommended)

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py seed_products
.\.venv\Scripts\python.exe manage.py createsuperuser
.\.venv\Scripts\python.exe manage.py runserver
```

Open http://127.0.0.1:8000/ and http://127.0.0.1:8000/admin/. If `py -3.13` is unavailable, install Python 3.13 or use a working Python 3.12+ interpreter.

`seed_products` adds 16 example products and can be run repeatedly without duplicates. Existing products are preserved; existing matching SKUs are not overwritten. Sample product graphics are SVG illustrations.

If upgrading an existing ShopEase folder, keep a backup of `db.sqlite3` and `media/` before replacing files. Do not commit your database, secrets, or personal uploads to a public GitHub repository.


## Redesigned UI
Orange marketplace storefront with campaign banners, flash sale, categories, and product cards. CSS uses Django staticfiles at `/static/shop/style.css`. If browser displays plain links, hard-refresh with Ctrl+F5 and verify `/static/shop/style.css` returns CSS.


## Product photos
Starter products use real photographs from Unsplash CDN, requiring internet access. They are illustrative and may not exactly match the product model. Upload your own images in Django Admin to override them. No AI-generated product illustrations are used in the starter catalog.
