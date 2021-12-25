
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from.import views

urlpatterns = [
    path('admin', admin.site.urls),
    path('', views.HOME, name='home'),
    path('base/', views.BASE, name='base'),
    path('products', views.PRODUCT, name='products'),
    path('products/<str:id>', views.PRODUCT_DETAILS, name='product_detail'),
    path('search/', views.SEARCH, name='search'),

    path('register', views.HandleRegister, name='register'),
    path('login', views.HandleLogin, name='login'),
    path('logout', views.HandleLogout, name='logout'),

    #Cart
    path('cart/add/<int:id>/', views.cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>/', views.item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>/',
         views.item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/',
         views.item_decrement, name='item_decrement'),
    path('cart/cart_clear/', views.cart_clear, name='cart_clear'),
    path('cart/cart-detail/',views.cart_detail,name='cart_detail'),

    path('cart/checkout/',views.CHECKOUT,name='checkout'),
    path('cart/checkout/placeorder',views.PLACE_ORDER,name='place_order'),

    path('success',views.SUCCESS, name='success'),


] + static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
