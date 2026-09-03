import json
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Category, Product, Cart, CartItem, Order, OrderItem

def index(request):
    return render(request, 'index.html')

def get_cart_from_request(request):
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
    else:
        if not request.session.session_key:
            request.session.create()
        session_id = request.session.session_key
        cart, _ = Cart.objects.get_or_create(session_id=session_id)
    return cart

def api_categories(request):
    categories = Category.objects.all()
    data = [{'id': c.id, 'name': c.name, 'slug': c.slug, 'icon': c.icon} for c in categories]
    return JsonResponse({'categories': data})

def api_products(request):
    category_slug = request.GET.get('category')
    search_query = request.GET.get('search')
    featured = request.GET.get('featured')

    products = Product.objects.all()

    if category_slug and category_slug != 'all':
        products = products.filter(category__slug=category_slug)

    if search_query:
        products = products.filter(name__icontains=search_query) | products.filter(description__icontains=search_query)

    if featured == 'true':
        products = products.filter(is_featured=True)

    data = []
    for p in products:
        data.append({
            'id': p.id,
            'name': p.name,
            'description': p.description,
            'price': float(p.price),
            'original_price': float(p.original_price) if p.original_price else None,
            'category_id': p.category.id,
            'category_name': p.category.name,
            'category_slug': p.category.slug,
            'image_url': p.image_url,
            'rating': p.rating,
            'reviews_count': p.reviews_count,
            'stock': p.stock,
            'is_featured': p.is_featured,
        })
    return JsonResponse({'products': data})

def api_product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    data = {
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'price': float(product.price),
        'original_price': float(product.original_price) if product.original_price else None,
        'category_name': product.category.name,
        'image_url': product.image_url,
        'rating': product.rating,
        'reviews_count': product.reviews_count,
        'stock': product.stock,
    }
    return JsonResponse({'product': data})

@csrf_exempt
def api_cart(request):
    cart = get_cart_from_request(request)

    if request.method == 'GET':
        items = []
        for item in cart.items.select_related('product').all():
            items.append({
                'id': item.id,
                'product_id': item.product.id,
                'name': item.product.name,
                'price': float(item.product.price),
                'image_url': item.product.image_url,
                'quantity': item.quantity,
                'subtotal': float(item.get_subtotal())
            })
        return JsonResponse({'items': items, 'total': float(cart.get_total())})

    elif request.method == 'POST':
        body = json.loads(request.body)
        product_id = body.get('product_id')
        quantity = int(body.get('quantity', 1))

        product = get_object_or_404(Product, id=product_id)
        item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            item.quantity += quantity
        else:
            item.quantity = quantity
        item.save()

        return JsonResponse({'message': 'Item added to cart', 'cart_count': sum(i.quantity for i in cart.items.all())})

    elif request.method == 'PUT':
        body = json.loads(request.body)
        item_id = body.get('item_id')
        quantity = int(body.get('quantity', 1))

        if quantity <= 0:
            CartItem.objects.filter(cart=cart, id=item_id).delete()
        else:
            CartItem.objects.filter(cart=cart, id=item_id).update(quantity=quantity)

        return JsonResponse({'message': 'Cart updated'})

    elif request.method == 'DELETE':
        body = json.loads(request.body or '{}')
        item_id = body.get('item_id')
        if item_id:
            CartItem.objects.filter(cart=cart, id=item_id).delete()
        else:
            cart.items.all().delete()
        return JsonResponse({'message': 'Cart cleared/item removed'})

@csrf_exempt
def api_checkout(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=400)

    cart = get_cart_from_request(request)
    if not cart.items.exists():
        return JsonResponse({'error': 'Cart is empty'}, status=400)

    body = json.loads(request.body)
    full_name = body.get('full_name')
    email = body.get('email')
    address = body.get('address')
    city = body.get('city')
    zip_code = body.get('zip_code')

    if not all([full_name, email, address, city, zip_code]):
        return JsonResponse({'error': 'All shipping fields are required'}, status=400)

    total = cart.get_total()

    order = Order.objects.create(
        user=request.user if request.user.is_authenticated else None,
        full_name=full_name,
        email=email,
        address=address,
        city=city,
        zip_code=zip_code,
        total_amount=total,
        status='Processing'
    )

    for item in cart.items.all():
        OrderItem.objects.create(
            order=order,
            product=item.product,
            price=item.product.price,
            quantity=item.quantity
        )

    # Clear cart
    cart.items.all().delete()

    return JsonResponse({
        'message': 'Order placed successfully!',
        'order_id': order.id,
        'total': float(order.total_amount),
        'status': order.status
    })

def api_orders(request):
    if not request.user.is_authenticated:
        return JsonResponse({'orders': []})

    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    data = []
    for order in orders:
        items = [{
            'product_name': i.product.name,
            'price': float(i.price),
            'quantity': i.quantity,
            'image_url': i.product.image_url
        } for i in order.items.all()]

        data.append({
            'id': order.id,
            'full_name': order.full_name,
            'total_amount': float(order.total_amount),
            'status': order.status,
            'created_at': order.created_at.strftime('%Y-%m-%d %H:%M'),
            'items': items
        })
    return JsonResponse({'orders': data})

@csrf_exempt
def api_register(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=400)
    body = json.loads(request.body)
    username = body.get('username')
    email = body.get('email')
    password = body.get('password')

    if User.objects.filter(username=username).exists():
        return JsonResponse({'error': 'Username already taken'}, status=400)

    user = User.objects.create_user(username=username, email=email, password=password)
    login(request, user)
    return JsonResponse({'message': 'Registration successful', 'user': {'username': user.username, 'email': user.email}})

@csrf_exempt
def api_login(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=400)
    body = json.loads(request.body)
    username = body.get('username')
    password = body.get('password')

    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return JsonResponse({'message': 'Login successful', 'user': {'username': user.username, 'email': user.email}})
    return JsonResponse({'error': 'Invalid credentials'}, status=400)

@csrf_exempt
def api_logout(request):
    logout(request)
    return JsonResponse({'message': 'Logged out'})

def api_me(request):
    if request.user.is_authenticated:
        return JsonResponse({'authenticated': True, 'user': {'username': request.user.username, 'email': request.user.email}})
    return JsonResponse({'authenticated': False})
