import uuid
from decimal import Decimal
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
import django.utils.timezone

class Migration(migrations.Migration):
    initial = True
    dependencies = [('auth', '0012_alter_user_first_name_max_length')]
    operations = [
        migrations.CreateModel(name='BaseUser', fields=[
            ('password', models.CharField(max_length=128, verbose_name='password')),
            ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
            ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
            ('username', models.CharField(error_messages={'unique':'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
            ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
            ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
            ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
            ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active.', verbose_name='active')),
            ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
            ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
            ('middle_name', models.CharField(blank=True, max_length=100)),
            ('gender', models.CharField(blank=True, max_length=30)),
            ('avatar', models.ImageField(blank=True, null=True, upload_to='avatars/')),
            ('email', models.EmailField(max_length=254, unique=True)),
            ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
            ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
        ], options={'db_table':'base_users'}, managers=[('objects', django.contrib.auth.models.UserManager())]),
        migrations.CreateModel(name='Product', fields=[
            ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
            ('name', models.CharField(max_length=200)),
            ('description', models.TextField(blank=True)),
            ('sku', models.CharField(max_length=50, unique=True)),
            ('price', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))])),
            ('stock', models.PositiveIntegerField(default=0)),
            ('thumbnail', models.ImageField(blank=True, null=True, upload_to='products/')),
            ('is_active', models.BooleanField(default=True)),
            ('created_at', models.DateTimeField(auto_now_add=True)),
            ('updated_at', models.DateTimeField(auto_now=True)),
        ], options={'db_table':'products','ordering':['-created_at']}),
        migrations.CreateModel(name='Cart', fields=[
            ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
            ('created_at', models.DateTimeField(auto_now_add=True)),
            ('updated_at', models.DateTimeField(auto_now=True)),
            ('owner', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='cart', to=settings.AUTH_USER_MODEL)),
        ], options={'db_table':'carts'}),
        migrations.CreateModel(name='Transaction', fields=[
            ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
            ('created_at', models.DateTimeField(auto_now_add=True)),
            ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='transactions', to=settings.AUTH_USER_MODEL)),
        ], options={'db_table':'transactions','ordering':['-created_at']}),
        migrations.CreateModel(name='CartProduct', fields=[
            ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
            ('quantity', models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)])),
            ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart_products', to='shop.cart')),
            ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart_products', to='shop.product')),
        ], options={'db_table':'cart_products'},),
        migrations.CreateModel(name='ProductTransaction', fields=[
            ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
            ('quantity', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
            ('unit_price', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
            ('item', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='product_transactions', to='shop.product')),
            ('transaction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_transactions', to='shop.transaction')),
        ], options={'db_table':'product_transactions'}),
        migrations.AddConstraint(model_name='cartproduct', constraint=models.UniqueConstraint(fields=('cart','product'), name='unique_cart_product')),
    ]
