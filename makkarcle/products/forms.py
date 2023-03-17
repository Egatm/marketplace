from django import forms
from django.forms import inlineformset_factory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, HTML
from .models import Product, Comment, ProductPhoto


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'description', 'price', 'image')

class ProductPhotoForm(forms.ModelForm):
    class Meta:
        model = ProductPhoto
        fields = ('photo', )

        def __init__(self, *args, **kwargs):
            super(ProductPhotoForm, self).__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.layout = Layout(
                Row(
                    Column('photo', css_class="col-md-10"),
                    Column(HTML('<button type="button" class="btn btn-danger remove-photo">Remove</button>'), css_class="col-md-2"),
                ),
            )
PhotoFormSet = inlineformset_factory(
    Product,
    ProductPhoto,
    form=ProductPhotoForm,
    fields=['photo',],
    extra=1,
    can_delete=True,
    max_num=None,
)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment',)
