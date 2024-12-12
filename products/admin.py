from django.contrib import admin

# Register your models here.
from .models import Product, Category, ProductVariant, Brand

admin.site.register([Product, Category, Brand, ProductVariant])