from django.contrib import admin
from .models import Category, Product, Comment


# Register your models here.
class CommentInLine(admin.TabularInline):
	model = Comment
	extra = 0


class ProductAdmin(admin.ModelAdmin):
	inlines = [
		CommentInLine,
	]


admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(Comment)
