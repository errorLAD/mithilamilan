from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse
import uuid

class Category(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=170, unique=True, blank=True)
    icon = models.CharField(max_length=50, default='fa-bag-shopping')
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Artist(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=170, unique=True, blank=True)
    photo = models.ImageField(upload_to='store/artists/', null=True, blank=True)
    location = models.CharField(max_length=150, help_text="e.g. Ranti Village, Madhubani")
    specialty = models.CharField(max_length=255, help_text="e.g. Master of Kachni & Bharni Madhubani Art")
    bio = models.TextField()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Product(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=285, unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    artist = models.ForeignKey(Artist, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    
    image = models.ImageField(upload_to='store/products/', null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    original_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="MRP price before discount")
    stock_quantity = models.IntegerField(default=10)
    
    short_description = models.TextField(help_text="Brief 2-line summary for product cards")
    full_description = models.TextField(help_text="Detailed product narrative")
    
    material = models.CharField(max_length=255, blank=True, help_text="e.g. Handmade Tussar Silk / Handmade Canvas Paper")
    dimensions = models.CharField(max_length=255, blank=True, help_text="e.g. 22 in x 15 in")
    art_style = models.CharField(max_length=255, blank=True, help_text="e.g. Traditional Bharni / Godna Mithila Painting")
    creation_details = models.TextField(blank=True, help_text="Handcrafted details, natural dyes used, etc.")
    artist_story = models.TextField(blank=True, help_text="Background of the artist or cultural motif")
    
    shipping_info = models.TextField(default="Free Express Shipping across India in 3-5 business days.")
    return_policy = models.TextField(default="7 Days Easy Returns & Replacement guarantee.")
    
    is_featured = models.BooleanField(default=False)
    is_bestseller = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    rating = models.FloatField(default=4.8)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_featured', '-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title) or 'product'
            slug = base_slug
            counter = 1
            while Product.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('store:product_detail', kwargs={'slug': self.slug})

    @property
    def discount_percentage(self):
        if self.original_price and self.original_price > self.price:
            disc = ((self.original_price - self.price) / self.original_price) * 100
            return int(round(disc))
        return 0

    @property
    def in_stock(self):
        return self.stock_quantity > 0

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='store/products/gallery/')
    caption = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Gallery image for {self.product.title}"

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name='carts')
    session_key = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart {self.pk} ({self.user.username if self.user else self.session_key})"

    @property
    def total_items(self):
        return sum(item.quantity for item in self.items.all())

    @property
    def subtotal(self):
        return sum(item.total_price for item in self.items.all())

    @property
    def delivery_charge(self):
        if self.subtotal > 999 or self.subtotal == 0:
            return 0
        return 99

    @property
    def grand_total(self):
        return self.subtotal + self.delivery_charge

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.title}"

    @property
    def total_price(self):
        return self.product.price * self.quantity

class Wishlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wishlist_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user.username} - {self.product.title}"

class Order(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('cod', 'Cash on Delivery (COD)'),
        ('upi', 'UPI / QR Code'),
        ('card', 'Credit/Debit Card / Netbanking'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
    ]

    ORDER_STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('confirmed', 'Order Confirmed'),
        ('packed', 'Packed'),
        ('shipped', 'Shipped'),
        ('out_for_delivery', 'Out for Delivery'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    order_number = models.CharField(max_length=50, unique=True, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    
    customer_name = models.CharField(max_length=150)
    customer_email = models.EmailField()
    customer_mobile = models.CharField(max_length=20)
    
    delivery_address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=20)
    
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_charge = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2)
    
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='cod')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    order_status = models.CharField(max_length=30, choices=ORDER_STATUS_CHOICES, default='pending')
    
    admin_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order #{self.order_number} by {self.customer_name}"

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = f"ORD-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    product_title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product_title} in #{self.order.order_number}"
