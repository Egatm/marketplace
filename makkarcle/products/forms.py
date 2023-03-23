from django import forms
from django.forms import inlineformset_factory, modelformset_factory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, HTML
from .models import Product, Comment, ProductPhoto


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'


class ProductPhotoForm(forms.ModelForm):
    class Meta:
        model = ProductPhoto
        fields = ('photo',)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment',)
