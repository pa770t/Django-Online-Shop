from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    category_image = models.ImageField(null=True, blank=True, upload_to='static/category_img')

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ManyToManyField(Category)
    name = models.CharField(max_length=255, null=False, blank=False)
    product_image = models.ImageField(null=True, blank=True, upload_to='static/product_img')
    price = models.DecimalField(max_digits=6, decimal_places=2, null=False, blank=False)
    featured = models.BooleanField(null=False, blank=False)
    inventory = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    profile_image = models.ImageField(default='static/profile_img/default.png', upload_to='static/profile_img')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField()
    total_price = models.DecimalField(max_digits=6, decimal_places=2)
    delivery_fee = models.IntegerField(null=False, blank=False, default=10)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"cart by {self.customer}"

class BillingAddress(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    mobile_no = models.CharField(max_length=100)
    address_line_one = models.CharField(max_length=255)
    address_line_two = models.CharField(max_length=255)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=255)
    zip_code = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"Billing Address of {self.first_name} {self.last_name}"

class Order(models.Model):
    status = (
        ('pending', 'Pending'),
        ('on the way', 'On the way'),
        ('delivered', 'Delivered')
    )
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    subtotal = models.DecimalField(max_digits=6, decimal_places=2)
    delivery_fee = models.IntegerField(null=False, blank=False, default=10)
    total = models.DecimalField(max_digits=6, decimal_places=2)
    billingaddress = models.OneToOneField(BillingAddress, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=50, choices=status, default=status[0])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.name
