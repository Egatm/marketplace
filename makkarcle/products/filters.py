import django_filters
from django_filters import NumberFilter, CharFilter
from .models import *


class ProductFilter(django_filters.FilterSet):
	start_price = NumberFilter(field_name="price", lookup_expr="gte", label="Минимальная цена")
	end_price = NumberFilter(field_name="price", lookup_expr="lte", label="Максимальная цена")
	firma = CharFilter(field_name="firma", lookup_expr="icontains", label="Производитель")
	name = CharFilter(field_name="name", lookup_expr="icontains", label="Наименование")

	class Meta:
		model = Product
		fields = [
			'category',
			'name',
			'firma',
			'start_price',
			'end_price',
		]