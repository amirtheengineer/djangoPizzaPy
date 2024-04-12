from django.contrib import admin

from menu.models import Pizza, Topping


# Register your models here.
@admin.register(Pizza)
class PizzaAdmin(admin.ModelAdmin):
    pass


@admin.register(Topping)
class ToppingAdmin(admin.ModelAdmin):
    pass