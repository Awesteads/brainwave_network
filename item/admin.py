from django.contrib import admin

#TUDO FAZ REFERENCIA A TELA DE ADMIN DO SITE

from .models import Category, Item

admin.site.register(Category)
admin.site.register(Item)