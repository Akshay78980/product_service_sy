from django.db import models
import uuid

from django.core.exceptions import ValidationError
from django.db.models import Q

import webcolors


# Create your models here.
    

class Category(models.Model):
    name = models.CharField(max_length=30, help_text="Enter category name (e.g., Hoodie, T-Shirt)")

    def __str__(self) -> str:
        return self.name
    
    def clean(self):
        if Category.objects.filter(Q(name__iexact=self.name) | Q(name__iexact=self.name + "s") | Q(name__iexact=self.name[:len(self.name)-1])).exists():
            raise ValidationError(f"A category with similar name already exists.")
        return super().clean()
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    
class Brand(models.Model):
    name=models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name
    
    def clean(self):
        if Brand.objects.filter(Q(name__iexact=self.name)).exists():
            raise ValidationError(f"A brand with similar name already exists.")
        return super().clean()
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)



class Product(models.Model):
    category = models.ForeignKey(Category, on_delete = models.CASCADE)
    product_id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    group_sku_number = models.CharField(max_length = 20, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self) -> str:
        return f'{self.name} ({self.group_sku_number})'
    
    class Meta:
        indexes = [
            models.Index(fields=['name'])
        ]
    
    def clean(self):
        if self.price:
            if self.price < 0:
                raise ValidationError("Product price cannot be less than zero.")


class ProductVariant(models.Model):

    SIZES = [
        ('S', 'S'),
        ('M', 'M'),
        ('L', 'L'),
        ('XL', 'XL'),
        ('XXL', 'XXL'),
        ('XXXL', 'XXXL'),
    ]
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    color = models.CharField(max_length=50, null=True, blank=True)
    size = models.CharField(max_length=20, choices=SIZES, null=True, blank=True, db_index=True)
    quantity = models.PositiveIntegerField()
    variant_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, db_index=True)
    image1 = models.ImageField(upload_to='product_images/')
    image2 = models.ImageField(upload_to='product_images/', null=True, blank=True)
    image3 = models.ImageField(upload_to='product_images/', null=True, blank=True)
    image4 = models.ImageField(upload_to='product_images/', null=True, blank=True)
    image5 = models.ImageField(upload_to='product_images/', null=True, blank=True)

    class Meta:
        unique_together = ['product','color','size']
        indexes = [
            models.Index(fields=['color'])
        ]

    def clean(self):
        if self.variant_price:
            if self.variant_price < 0:
                raise ValidationError("Variant price cannot be negative.")
            if self.product.price:
                if self.variant_price < self.product.price:
                    raise ValidationError("Variant price cannot be less than the base price of the product.")

        if self.color:
            self.color = self.color.strip().lower()
            try:
                self.color = webcolors.name_to_hex(self.color)
            except ValueError:
                if self.color.startswith('#') and len(self.color) in (4, 7): 
                    if len(self.color) == 4:
                        self.color = "#" + "".join([i*2 for i in self.color[1:]]) 
                    try:
                        webcolors.hex_to_name(self.color)
                    except ValueError:
                        raise ValidationError("Invalid hex color code.")
                else:
                    raise ValidationError("Invalid color format. Please provide a valid color name or hex code.")

        return super().clean()

    def __str__(self):
        return f'{self.product.__str__()} - {self.color}'

