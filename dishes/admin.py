from django.contrib import admin

from dishes.models import Category, Dish


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name", )}
    list_display = ["name", ]


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name", )}
    list_display = ["name", "description", "kitchen_type", "composition", "weight", "caloric",
                    "image", "price", "discount", "spice", ]
