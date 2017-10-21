from django.contrib import admin

# Register your models here.
from store.models import Item


class ItemsListAdmin(admin.ModelAdmin):
    list_display = ["title", "price", "content", "number", "id"]
    list_filter = ["title", "number"]
    list_editable = ["number", "price"]

    search_fields = ["title", "content"]

    class Meta:
        model = Item


admin.site.register(Item, ItemsListAdmin)
