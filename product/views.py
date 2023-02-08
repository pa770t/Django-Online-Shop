from django.shortcuts import render, redirect
from .models import *
from django.http import HttpResponse, Http404
from django.db.models import Q
from .forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.core.paginator import Paginator, EmptyPage

from .decorators import *

# Create your views here.

def home(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    featured_products = Product.objects.filter(featured=True).order_by('?')[:6]
    latest_products = Product.objects.all().order_by('-created_at')[:6]

    return render(request, 'index.html', {
        'products': products,
        'categories': categories,
        'featured_products': featured_products,
        'latest_products': latest_products,
    })

@customer_only
def category(request):
    return HttpResponse('category page')

def shop(request):
    products = Product.objects.all().order_by('?')
    page = request.GET.get('page', default=1)
    items = request.GET.get('items', default=4)
    if items == 10:
        items = 10
    elif items == 20:
        items = 20
    elif items == 30:
        items = 30

    if request.GET:
        search = request.GET.get('s', '')
        category = request.GET.get('category', '')
        sort_by = request.GET.get('sort_by', '')

        cheap = request.GET.get('cheap', '')
        fair = request.GET.get('fair', '')
        expensive = request.GET.get('expensive', '')

        if search:
            products = products.filter(name__icontains=search).order_by('?')

        elif category:
            try:
                category = Category.objects.get(name=category)
                products = products.filter(category=category).order_by('?')
            except:
                products = []
        
        elif sort_by == 'latest' or sort_by == 'popularity' or sort_by == 'best-rating':
            if sort_by == 'latest':
                products = products.order_by('-created_at')

            if sort_by == 'popularity':
                products = products.filter(featured=True)

            if sort_by == 'best-rating':
                products = products.filter(featured=True)

        elif cheap or fair or expensive:
            if cheap and fair and expensive:
                products = Product.objects.all()
            elif cheap and fair:
                products = products.filter(price__lte=300)
            elif cheap and expensive:
                products = products.filter(Q(price__lte=200) | Q(price__gt=400))
            elif fair and expensive:
                products = products.filter(price__gt=300)
            elif fair:
                products = products.filter(Q(price__lt=500) & Q(price__gt=200))
            elif expensive:
                products = products.filter(price__gt=500)
            else:
                products = products.filter(price__lte=200)

        elif not page:
            return render(request, '404.html', status=404)

    if products:
        perpage = items
        paginator = Paginator(products, per_page=perpage)
        try:
            products = paginator.page(number=page)
            pagination = paginator.get_page(page)
            num_pages = "i" * pagination.paginator.num_pages
        except EmptyPage:
            products = []
        return render(request, 'shop.html', {
            'products': products,
            'pagination': pagination,
            'num_pages': num_pages
        })
    else:
        return render(request, '404.html', status=404)

def shop_detail(request, id):
    try:
        product = Product.objects.get(id=id)
        featured_products = Product.objects.filter(featured=True)
        return render(request, 'detail.html', {
            'product': product,
            'featured_products': featured_products,
        })
    except:
        return render(request, '404.html', status=404)

@login_required(login_url='login_user')
@customer_only
def cart(request):
    cart_items = Cart.objects.filter(customer=request.user.customer).order_by('-created_date')
    delivery_fee = 0
    subtotal = 0
    total = 0

    for item in cart_items:
        subtotal = subtotal + item.product.price
        delivery_fee = item.delivery_fee
        total = subtotal + delivery_fee
    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total_cart': cart_items.count(),
        'subtotal': subtotal,
        'delivery_fee': delivery_fee,
        'total': total
    })

@login_required(login_url='login_user')
@customer_only
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    # add to cart
    Cart.objects.create(product=product, customer=request.user.customer, quantity=1, total_price=0)
    return redirect('cart')

@customer_only
def delete_cart(request, product_id):
    cart = Cart.objects.get(id=product_id)
    # delete cart
    cart.delete()
    messages.success(request, f'Successfully deleted "{cart.product}"!')
    return redirect('cart')

@authenticated_user
def register_user(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # login user
            login(request, user)
            return redirect('home')

    return render(request, 'register.html', {
        'form': form
    })

@authenticated_user
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.groups.filter(name='Manager'):
                login(request, user)
                return redirect('dashboard')
            else:
                login(request, user)
                return redirect('home')
        else:
            messages.error(request, 'Username and Password is incorrect!')
            return redirect('login_user')
    return render(request, 'login.html')

@login_required(login_url='login_user')
def logout_user(request):
    logout(request)
    return redirect('login_user')

@login_required(login_url='login_user')
@customer_only
def profile_setting(request):
    user = User.objects.get(username=request.user)
    profile_form = ProfileSettingForm(instance=user)
    customer = Customer.objects.get(user=request.user)
    customer_form = CustomerForm(instance=customer)

    if request.method == 'POST':
        data = request.POST
        image = request.FILES

        profile_form = ProfileSettingForm(data, instance=user)
        customer_form = CustomerForm(data, image, instance=customer)
        if profile_form.is_valid() and customer_form.is_valid():
            profile_form.save()
            print(customer_form.data)
            customer_form.save()
            return redirect('home')

    return render(request, 'profile_setting.html', {
        'profile_form': profile_form,
        'customer_form': customer_form,
    })

@login_required(login_url='login_user')
@customer_only
def checkout(request):
    carts = Cart.objects.filter(customer=request.user.customer)
    cart_subtotal = 0
    delivery_fee = 0
    cart_total = 0

    order_subtotal = 0

    for cart in carts:
        cart_subtotal += cart.product.price
        delivery_fee = cart.delivery_fee
        cart_total = cart_subtotal + delivery_fee

        order_subtotal = cart.product.price
        order_total = order_subtotal + delivery_fee

    form = BillingAddressForm()
    if request.method == 'POST':
        form = BillingAddressForm(request.POST)
        if form.is_valid():

            carts = Cart.objects.filter(customer=request.user.customer)
            cart_subtotal = 0
            delivery_fee = 0
            cart_total = 0

            order_subtotal = 0

            if carts:
                for cart in carts:
                    cart_subtotal = cart.product.price
                    delivery_fee = cart.delivery_fee
                    cart_total = cart_subtotal + delivery_fee

                    order_subtotal = cart.product.price
                    order_total = order_subtotal + delivery_fee

                    # save the form
                    form=BillingAddressForm(request.POST)
                    billingaddress = form.save()

                    # create order
                    order = Order.objects.create(product=cart.product, customer=cart.customer, subtotal=order_subtotal, delivery_fee=delivery_fee, total=order_total, billingaddress=billingaddress)
                    

                # delete cart after creating orders
                carts.delete()
                messages.info(request, 'You ordered Successfully!')
                return redirect('cart')
            else:
                return render(request, '404.html', status=404)

    return render(request, 'checkout.html', {
        'carts': carts,
        'subtotal': cart_subtotal,
        'delivery_fee': delivery_fee,
        'total': cart_total,
        'form': form
    })

@login_required(login_url='login_user')
@customer_only
def add_order(request):
    carts = Cart.objects.filter(customer=request.user.customer)
    subtotal = 0
    total = 0

    for cart in carts:
        print(cart.product)
        print(cart.product.price)

    return redirect('cart')

# Managers only views

@login_required(login_url='login_user')
@manager_only
def dashboard(request):
    total_product = Product.objects.count()
    total_order = Order.objects.count()
    total_customer = Customer.objects.count()
    return render(request, 'dashboard.html', {
        'total_product': total_product,
        'total_order': total_order,
        'total_customer': total_customer
    })

@login_required(login_url='login_user')
@manager_only
def product_manager_view(request):
    products = Product.objects.all()
    total = Product.objects.count()
    return render(request, 'product_manager_view.html', {
        'products': products,
        'total': total
    })

@login_required(login_url='login_user')
@manager_only
def delete_product(request, product_id):
    product = Product.objects.get(id=product_id)
    product.delete()
    return redirect('product_manager_view')

@login_required(login_url='login_user')
@manager_only
def product_delete_manager_view(request, product_id):
    product = Product.objects.get(id=product_id)
    return render(request, 'product_delete_manager_view.html', {
        'product': product
    })

@login_required(login_url='login_user')
@manager_only
def order_manager_view(request):
    total_order = Order.objects.count()
    customers = Customer.objects.all()
    return render(request, 'order_manager_view.html', {
        'customers': customers,
        'total_order': total_order
    })

@login_required(login_url='login_user')
@manager_only
def orders_by_customer_manager_view(request, customer_id):
    customer = Customer.objects.get(id=customer_id)
    orders = customer.order_set.all()
    if orders:
        return render(request, 'orders_by_customer_manager_view.html', {
            'orders': orders
        })
    else:
        return render(request, '404.html', status=404)

@login_required(login_url='login_user')
@manager_only
def delete_order_by_manager(request, order_id):
    # Delete order
    Order.objects.get(id=order_id).delete()
    return redirect('order_manager_view')

@login_required(login_url='login_user')
@manager_only
def order_delete_by_customer_manager_view(request, order_id):
    order = Order.objects.get(id=order_id)
    return render(request, 'order_delete_by_customer_manager_view.html', {
        'order': order
    })

@login_required(login_url='login_user')
@manager_only
def customer_manager_view(request):
    customers = Customer.objects.all()
    total = Customer.objects.count()
    return render(request, 'customer_manager_view.html', {
        'customers': customers,
        'total': total
    })

@login_required(login_url='login_user')
@manager_only
def only_customer_manager_view(request, customer_id):
    customer = Customer.objects.get(id=customer_id)
    total_cart = Cart.objects.filter(customer=customer).count()
    total_order = Order.objects.filter(customer=customer).count()
    return render(request, 'only_customer_manager_view.html', {
        'customer': customer,
        'total_cart': total_cart,
        'total_order': total_order
    })
