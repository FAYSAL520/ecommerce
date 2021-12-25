from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from store_app.models import Product, Categories, Filter_Price, Color, Brand, Order,OrderItem
from django.contrib.auth.decorators import login_required
from django.conf import settings
from cart.cart import Cart
from django.views.decorators.csrf import csrf_exempt
import razorpay

client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID,settings.RAZORPAY_KEY_SECRECT))



def BASE(request):
    categories = Categories.objects.all()
    context = {
        'categories': categories,
    }
    return render(request, 'main/base.html', context)


def HOME(request):
    product = Product.objects.filter(status = 'Publish')
    categories = Categories.objects.all()

    context = {
        'product':product,
        'categories': categories,
    }
    return render(request, 'main/index.html',context)


def PRODUCT(request):

    categories = Categories.objects.all()
    filter_price = Filter_Price.objects.all()
    color = Color.objects.all()
    brand = Brand.objects.all()

    CATID = request.GET.get('categories')
    BRANDID = request.GET.get('brand')
    PRICEID = request.GET.get('price_range')
    COLORID = request.GET.get('color')

    ATOZID = request.GET.get('ATOZ')
    ZTOAID = request.GET.get('ZTOA')
    PRICE_LOWTOHIGHID = request.GET.get('PRICE_LOWTOHIGH')
    PRICE_HIGHTOLOWID = request.GET.get('PRICE_HIGHTOLOW')
    NEW_PRODUCTID = request.GET.get('NEW_PRODUCT')
    OLD_PRODUCTID = request.GET.get('OLD_PRODUCT')

    if CATID:
        product = Product.objects.filter(categories = CATID, status='Publish')
    elif BRANDID:
        product = Product.objects.filter(brand=BRANDID, status='Publish')
    elif PRICEID:
        product = Product.objects.filter(filter_price=PRICEID, status='Publish')
    elif COLORID:
        product = Product.objects.filter(color=COLORID, status='Publish')
    elif ATOZID:
        product = Product.objects.filter(status='Publish').order_by('name')
    elif ZTOAID:
        product = Product.objects.filter(status='Publish').order_by('-name')
    elif PRICE_LOWTOHIGHID:
        product = Product.objects.filter(status='Publish').order_by('price')
    elif PRICE_HIGHTOLOWID:
        product = Product.objects.filter(status='Publish').order_by('-price')
    elif NEW_PRODUCTID:
        product = Product.objects.filter(status='Publish', condition='New').order_by('-id')
    elif OLD_PRODUCTID:
        product = Product.objects.filter(status='Publish', condition='Old').order_by('-id')
    else:
        product = Product.objects.filter(status = 'Publish').order_by('-id')

    context = {
        'product': product,
        'categories': categories,
        'filter_price': filter_price,
        'color': color,
        'brand': brand,
    }

    return render(request, 'main/product.html', context)


def SEARCH(request):
    categories = Categories.objects.all()
    Query = request.GET.get('query')
    product = Product.objects.filter(name__icontains = Query)

    context = {
        'categories': categories,
        'product': product,
    }
    return render(request, 'main/search.html', context)


def PRODUCT_DETAILS(request,id):
    produc = Product.objects.filter(id = id).first()
    color = Color.objects.all()

    context = {
        'produc': produc,
        'color': color,
    }

    return render(request, 'main/product_single.html', context)


def HandleRegister(request):
    if request.method == "POST":
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')

        customer = User.objects.create_user(username,email,pass1)
        customer.first_name = first_name
        customer.last_name = last_name
        customer.save()
        return redirect('home')

    return render(request, 'Registration/auth.html')


def HandleLogin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username = username,password = password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            return redirect('login')


    return render(request, 'Registration/auth.html')


def HandleLogout(request):
    logout(request)

    return redirect('home')







@login_required(login_url="/login")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("home")


@login_required(login_url="/login")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="/login")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/login")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url="/login")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="/login")
def cart_detail(request):
    return render(request, 'Cart/cart_details.html')


def CHECKOUT(request):
    amount_str = request.POST.get('amount')
    amount_float = float(amount_str)
    amount = int(amount_float)
    payment = client.order.create({
        "amount": amount,
        "currency": "INR",
        "payment_capture":"1"
    }) 
    order_id = payment['id']
    context = {
        'order_id':order_id,
        'payment':payment,
    }
    return render(request, 'Cart/checkout.html',context)


def PLACE_ORDER(request):
    if request.method == "POST":
        uid = request.session.get('_auth_user_id')
        user = User.objects.get(id = uid)
        cart = request.session.get('cart')

        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        country = request.POST.get('country')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        postcode = request.POST.get('postcode')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        additional_info = request.POST.get('additional_info')
        amount = request.POST.get('amount')

        order_id = request.POST.get('order_id')
        payment = request.POST.get('payment')

        context = {
            'order_id': order_id,
        }

        order = Order(
            user = user,
            firstname = firstname,
            lastname = lastname,
            country = country,
            address = address,
            city = city,
            state = state,
            postcode = postcode,
            phone = phone,
            email = email,
            additional_info =additional_info,
            payment_id =order_id,
            amount =amount,
        )
        order.save()
        for i in cart:
            a = (int(cart[i]['price']))
            b = cart[i]['quantity']
            total = a * b


            item = OrderItem(
                order = order,
                product = cart[i]['name'],
                image = cart[i]['image'],
                quantity = cart[i]['quantity'],
                price = cart[i]['price'],
                total = total,
            )
            item.save()

        return render(request,'Cart/placeorder.html',context)


@csrf_exempt
def SUCCESS(request):
    if request.method == "POST":
        a = request.POST
        order_id = ""
        for key, val in a.items():
            if key == 'razorpay_order_id':
                order_id = val
                break
        user = Order.objects.filter(payment_id = order_id).first()
        user.paid = True
        user.save()

    return render(request, 'Cart/thank_you.html')