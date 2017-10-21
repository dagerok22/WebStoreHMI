from django.contrib import admin

# Register your models here.
from store.models import Item, Bucket, Order


class ItemsListAdmin(admin.ModelAdmin):
    list_display = ["title", "price", "content", "number", "id"]
    list_filter = ["title", "number"]
    list_editable = ["number", "price"]

    search_fields = ["title", "content"]

    class Meta:
        model = Item


admin.site.register(Item, ItemsListAdmin)


class BucketsListAdmin(admin.ModelAdmin):
    list_display = ["user"]
    search_fields = ["user"]

    class Meta:
        model = Bucket


admin.site.register(Bucket, BucketsListAdmin)


class OrderListAdmin(admin.ModelAdmin):
    list_display = ["user", "status", "date"]
    list_filter = ["user", "date"]
    list_editable = ["status"]

    search_fields = ["user"]

    class Meta:
        model = Bucket


admin.site.register(Order, OrderListAdmin)
