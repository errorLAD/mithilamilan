from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Category, Artist, Product, ProductImage, Cart, CartItem, Wishlist, Order, OrderItem
from .forms import CheckoutForm

def _get_or_create_cart(request):
    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key

    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        cart, created = Cart.objects.get_or_create(session_key=session_key)
    return cart

def store_home(request):
    categories = Category.objects.all()
    featured_products = Product.objects.filter(is_active=True, is_featured=True)[:6]
    bestsellers = Product.objects.filter(is_active=True, is_bestseller=True)[:6]
    new_arrivals = Product.objects.filter(is_active=True).order_by('-created_at')[:6]
    artists = Artist.objects.all()[:4]
    cart = _get_or_create_cart(request)

    context = {
        'categories': categories,
        'featured_products': featured_products,
        'bestsellers': bestsellers,
        'new_arrivals': new_arrivals,
        'artists': artists,
        'cart': cart,
    }
    return render(request, 'store/store_home.html', context)

def product_list(request):
    query = request.GET.get('q', '').strip()
    category_slug = request.GET.get('category', '').strip()
    artist_slug = request.GET.get('artist', '').strip()
    sort_by = request.GET.get('sort', 'newest').strip()
    in_stock_only = request.GET.get('in_stock', '').strip()

    products_qs = Product.objects.filter(is_active=True)

    if query:
        products_qs = products_qs.filter(
            Q(title__icontains=query) |
            Q(short_description__icontains=query) |
            Q(full_description__icontains=query) |
            Q(material__icontains=query) |
            Q(art_style__icontains=query)
        )

    if category_slug:
        products_qs = products_qs.filter(category__slug=category_slug)

    if artist_slug:
        products_qs = products_qs.filter(artist__slug=artist_slug)

    if in_stock_only == 'true' or in_stock_only == '1':
        products_qs = products_qs.filter(stock_quantity__gt=0)

    if sort_by == 'price_low':
        products_qs = products_qs.order_by('price')
    elif sort_by == 'price_high':
        products_qs = products_qs.order_by('-price')
    elif sort_by == 'rating':
        products_qs = products_qs.order_by('-rating')
    else:
        products_qs = products_qs.order_by('-created_at')

    categories = Category.objects.all()
    artists = Artist.objects.all()

    paginator = Paginator(products_qs, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    cart = _get_or_create_cart(request)

    context = {
        'products': page_obj,
        'page_obj': page_obj,
        'categories': categories,
        'artists': artists,
        'query': query,
        'selected_category': category_slug,
        'selected_artist': artist_slug,
        'sort_by': sort_by,
        'in_stock_only': in_stock_only,
        'total_count': products_qs.count(),
        'cart': cart,
    }
    return render(request, 'store/product_list.html', context)

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    gallery_images = product.images.all()
    related_products = Product.objects.filter(is_active=True, category=product.category).exclude(pk=product.pk)[:4]
    
    in_wishlist = False
    if request.user.is_authenticated:
        in_wishlist = Wishlist.objects.filter(user=request.user, product=product).exists()

    cart = _get_or_create_cart(request)

    context = {
        'product': product,
        'gallery_images': gallery_images,
        'related_products': related_products,
        'in_wishlist': in_wishlist,
        'cart': cart,
    }
    return render(request, 'store/product_detail.html', context)

def cart_view(request):
    cart = _get_or_create_cart(request)
    cart_items = cart.items.select_related('product').all()
    context = {
        'cart': cart,
        'cart_items': cart_items,
    }
    return render(request, 'store/cart.html', context)

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id, is_active=True)
    cart = _get_or_create_cart(request)
    qty = int(request.POST.get('quantity', 1))

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += qty
    else:
        cart_item.quantity = qty
    
    if cart_item.quantity > product.stock_quantity:
        cart_item.quantity = product.stock_quantity
        messages.warning(request, f"Adjusted quantity to max available stock ({product.stock_quantity}).")

    cart_item.save()
    messages.success(request, f"Added '{product.title}' to your cart!")
    
    next_url = request.POST.get('next') or request.META.get('HTTP_REFERER') or 'store:cart_view'
    return redirect(next_url)

def update_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, pk=item_id)
    action = request.POST.get('action')

    if action == 'increase':
        if cart_item.quantity < cart_item.product.stock_quantity:
            cart_item.quantity += 1
            cart_item.save()
    elif action == 'decrease':
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()

    return redirect('store:cart_view')

def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, pk=item_id)
    title = cart_item.product.title
    cart_item.delete()
    messages.info(request, f"Removed '{title}' from your cart.")
    return redirect('store:cart_view')

@login_required
def wishlist_view(request):
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('product')
    cart = _get_or_create_cart(request)
    return render(request, 'store/wishlist.html', {'wishlist_items': wishlist_items, 'cart': cart})

@login_required
def toggle_wishlist(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    item, created = Wishlist.objects.get_or_create(user=request.user, product=product)
    
    if not created:
        item.delete()
        messages.info(request, f"Removed '{product.title}' from your wishlist.")
    else:
        messages.success(request, f"Saved '{product.title}' to your wishlist!")

    next_url = request.META.get('HTTP_REFERER') or 'store:wishlist_view'
    return redirect(next_url)

def checkout_view(request):
    cart = _get_or_create_cart(request)
    cart_items = cart.items.select_related('product').all()

    if not cart_items:
        messages.warning(request, "Your shopping cart is empty.")
        return redirect('store:store_home')

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            
            order.subtotal = cart.subtotal
            order.delivery_charge = cart.delivery_charge
            order.grand_total = cart.grand_total
            order.save()

            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    product_title=item.product.title,
                    price=item.product.price,
                    quantity=item.quantity,
                    subtotal=item.total_price
                )
                # Deduct stock
                item.product.stock_quantity = max(0, item.product.stock_quantity - item.quantity)
                item.product.save()

            # Clear cart
            cart.items.all().delete()

            messages.success(request, f"Order #{order.order_number} placed successfully!")
            return redirect('store:order_detail', order_number=order.order_number)
    else:
        initial_data = {}
        if request.user.is_authenticated:
            initial_data = {
                'customer_name': request.user.get_full_name() or request.user.username,
                'customer_email': request.user.email,
            }
        form = CheckoutForm(initial=initial_data)

    context = {
        'cart': cart,
        'cart_items': cart_items,
        'form': form,
    }
    return render(request, 'store/checkout.html', context)

def order_history(request):
    orders = []
    if request.user.is_authenticated:
        orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    cart = _get_or_create_cart(request)
    return render(request, 'store/order_history.html', {'orders': orders, 'cart': cart})

def order_detail(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)
    items = order.items.all()
    cart = _get_or_create_cart(request)

    if request.method == 'POST' and request.POST.get('action') == 'cancel':
        if order.order_status in ['pending', 'confirmed']:
            order.order_status = 'cancelled'
            order.save()
            messages.info(request, f"Order #{order.order_number} has been cancelled.")
            return redirect('store:order_detail', order_number=order.order_number)

    context = {
        'order': order,
        'items': items,
        'cart': cart,
    }
    return render(request, 'store/order_detail.html', context)
