from django.contrib import admin

# Register your models here.
from .models import *

class ImagesTublerinline(admin.TabularInline):
    model = Images

class TagTublerinline(admin.TabularInline):
    model = Tag

class ProductAdmin(admin.ModelAdmin):
    inlines = [ImagesTublerinline,TagTublerinline]

class OrderItemTublerinline(admin.TabularInline):
    model = OrderItem

class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemTublerinline]
    list_display = ['user', 'phone', 'email', 'payment_id', 'paid', 'date']




admin.site.register(Images)
admin.site.register(Tag)

admin.site.register(Categories)
admin.site.register(Brand)
admin.site.register(Color)
admin.site.register(Filter_Price)
admin.site.register(Product,ProductAdmin)

admin.site.register(Order,OrderAdmin)
admin.site.register(OrderItem)
