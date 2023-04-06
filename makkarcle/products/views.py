from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, FormView
from django.views.generic.edit import UpdateView, DeleteView
from django.views.generic.detail import SingleObjectMixin
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from datetime import date
from .models import Product, ProductPhoto, Order, OrderItem
from .forms import CommentForm, ProductPhotoForm, ProductForm
from .filters import ProductFilter
from django.forms import inlineformset_factory
from django.contrib.auth.decorators import login_required
from django.contrib import messages


# создание inline-формы для связи нескольких объектов ProductPhoto с одним объектом Product
ProductPhotoFormSet = inlineformset_factory(Product, ProductPhoto, form=ProductPhotoForm, extra=1, can_delete=False)


# создание класса для отображения формы создания нового объекта Product с несколькими формами ProductPhoto
class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'product_new.html'

    # переопределение метода get_context_data для добавления inline-формы в контекст шаблона
    def get_context_data(self, **kwargs):
        context = super(ProductCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = ProductPhotoFormSet(self.request.POST, self.request.FILES, prefix='productphoto')
        else:
            context['formset'] = ProductPhotoFormSet(queryset=ProductPhoto.objects.none(), prefix='productphoto')
        return context

    # переопределение метода form_valid для сохранения объекта Product и объектов ProductPhoto, связанных с ним
    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            response = super().form_valid(form)
            formset.instance = self.object
            formset.save()
            return response
        else:
            return self.render_to_response(self.get_context_data(form=form))


# отображение списка товаров
class ProductsListView(ListView):
    model = Product
    template_name = "product_list.html"

    # фильтрация списка товаров по поисковому запросу
    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('search')
        if query:
            queryset = queryset.filter(Q(name__icontains=query) | Q(description__icontains=query))
        return queryset

    # добавление в контекст текущей даты и объекта фильтра для списка товаров
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['today'] = date.today()

        products = self.get_queryset()
        my_filter = ProductFilter(self.request.GET, queryset=products)

        if my_filter.form.is_valid():
            products = my_filter.qs
        context['product_list'] = products
        context['filter'] = my_filter

        return context


# отображение детальной информации о товаре и добавление комментария
class CommentGet(DetailView):
    model = Product
    template_name = "product_detail.html"

    # добавление формы комментария в контекст
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        return context


# добавление комментария к товару
class CommentPost(SingleObjectMixin, FormView):
    model = Product
    form_class = CommentForm
    template_name = "product_detail.html"

    # получение объекта Product
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    # сохранение комментария
    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.product = self.object
        comment.author = self.request.user
        comment.save()
        return super().form_valid(form)

    # перенаправление пользователя на страницу товара после добавления комментария
    def get_success_url(self):
        product = self.get_object()
        return reverse("product_detail", kwargs={"pk": product.pk})


# отображение детальной информации о товаре и обработка комментариев
class ProductsDetailView(View):
    # отображение страницы товара с формой комментария при GET-запросе
    def get(self, request, *args, **kwargs):
        view = CommentGet.as_view()
        return view(request, *args, **kwargs)

    # добавление комментария при POST-запросе
    def post(self, request, *args, **kwargs):
        view = CommentPost.as_view()
        return view(request, *args, **kwargs)


# редактирование информации о товаре
class ProductsUpdateView(UpdateView):
    model = Product
    fields = (
        "category",
        "firma",
        "name",
        "description",
        "description_all",
        "price",
    )
    template_name = "product_edit.html"


# удаление товара
class ProductsDeleteView(DeleteView):
    model = Product
    template_name = "product_delete.html"
    success_url = reverse_lazy("product_list")


# Эта функция позволяет добавить товар в корзину
@login_required
def add_to_cart(request, id):
    # Находим товар по id
    product = Product.objects.get(id=id)
    # Ищем заказ соответствующий этому пользователю и товару
    # Если такой заказ существует, то используем его, в противном случае создаем новый
    order, created = Order.objects.get_or_create(
         user=request.user,
         product=product,
         defaults={'quantity': 1}
    )
    # Если заказ уже был создан ранее, то увеличиваем его количество на 1 и сохраняем его
    if not created:
        order.quantity += 1
        order.save()
    # Добавляем сообщение об успешном добавлении товара в корзину
    messages.success(request, "Товар добавлен в корзину.")
    # Перенаправляем на страницу корзины
    return redirect('cart')


# Эта функция отображает содержимое корзины
@login_required
def cart(request):
    # Извлекаем все заказы данного пользователя
    orders = Order.objects.filter(user=request.user)
    # Вычисляем общую стоимость товаров в корзине
    total_price = calculate_cart_price(orders)
    # Создаем контекст для отображения корзины
    context = {'orders': orders, 'total_price': total_price}
    # Отображаем корзину с помощью html-шаблона
    return render(request, 'cart.html', context)


# Эта функция удаляет товар из корзины
@login_required
def remove_from_cart(request, id):
    # Находим заказ по id и удаляем его
    order = Order.objects.get(id=id)
    order.delete()
    # Добавляем сообщение об успешном удалении товара из корзины
    messages.success(request, "Товар удален из корзины.")
    # Перенаправляем на страницу корзины
    return redirect('cart')


# Эта функция позволяет изменить количество товара в корзине
def change_quantity(request, pk):
    # Извлекаем заказ по его id
    order = get_object_or_404(Order, pk=pk)
    # Если метод запроса - POST, то получаем новое значение количества товаров
    if request.method == 'POST':
        new_quantity = request.POST.get('quantity')
        # Если новое значение больше 0, то сохраняем его и обновляем заказ
        if int(new_quantity) > 0:
            order.quantity = int(new_quantity)
            order.save()
    # Перенаправляем на страницу корзины
    return redirect('cart')


# Эта функция вычисляет общую стоимость всех товаров в корзине
def calculate_cart_price(orders):
    total_price = 0
    for order in orders:
        total_price += order.total_price()
    return total_price


@login_required
# Эта функция позволяет просмотреть содержимое корзины
def view_cart(request):
    # Извлекаем все заказы данного пользователя
    orders = Order.objects.filter(user=request.user)
    # Отбираем только те заказы, у которых есть товары
    new_orders = []
    for order in orders:
        if order.order_items.first():
            new_orders.append(order)
    # Если в корзине нет товаров, то возвращаем сообщение об этом
    if not new_orders:
        return render(request, 'cart.html', {'message': 'Ваша корзина пуста.'})
    # Вычисляем общую стоимость товаров в корзине
    total_price = round(calculate_cart_price(new_orders), 2)
    # Создаем контекст для отображения корзины
    context = {
        'orders': new_orders,
        'total_price': total_price,
    }
    # Отображаем корзину с помощью html-шаблона
    return render(request, 'cart.html', context)


@login_required
def checkout(request):
    # получаем все заказы пользователя из базы данных
    orders = Order.objects.filter(user=request.user)
    # вычисляем общую стоимость заказов
    total_price = calculate_cart_price(orders)

    # если метод запроса POST, то создаем новый OrderItem объект на основе каждого заказа
    if request.method == 'POST':
        for order in orders:
            # создаем новый OrderItem объект на основе текущего заказа и связываем его с созданным Order
            order_item = OrderItem.objects.create(
                product=order.product,
                quantity=order.quantity,
                user=request.user
            )
            # удаляем текущий Order объект из базы данных
            order.delete()

        # выводим сообщение об успешном оформлении заказа
        messages.success(request, "Заказ оформлен. С вами свяжутся для подтверждения.")
        # перенаправляем на страницу с заказами пользователя
        return redirect('my_orders')

    # передаем в контекст все заказы и общую стоимость для отображения пользователю на странице оформления заказа
    context = {
        'orders': orders,
        'total_price': total_price,
    }
    # рендерим шаблон страницы оформления заказа с полученным контекстом
    return render(request, 'checkout.html', context)


@login_required
def my_orders(request):
    # получаем все заказы пользователя из базы данных и сортируем их по убыванию идентификационного номера
    orders = OrderItem.objects.filter(user=request.user).order_by('-id')

    # вычисляем общую стоимость всех заказов пользователя
    total_price = sum(order.total_price() for order in orders)

    # передаем в контекст все заказы и их общую стоимость для отображения пользователю на странице с его заказами
    context = {
        'orders': orders,
        'total_price': total_price,
    }
    # рендерим шаблон страницы с заказами пользователя с полученным контекстом
    return render(request, 'my_orders.html', context)


# принимаем запрос на отмену заказа с указанным идентификационным номером
def cancel_order(request, pk):
    # получаем объект заказа по его идентификационному номеру или выдаем ошибку 404, если такого заказа нет
    order = get_object_or_404(OrderItem, pk=pk)

    # если метод запроса POST и в запросе есть параметр 'confirm' со значением 'yes', то удаляем заказ из базы данных
    if request.method == 'POST' and request.POST.get('confirm') == 'yes':
        order.delete()
        # выводим сообщение об успешной отмене заказа
        messages.success(request, 'Заказ успешно отменен.')
        # перенаправляем на страницу с заказами пользователя
        return redirect('my_orders')

    # передаем в контекст заказ, который будет отменен, для отображения пользователю на странице с подтверждением
    # отмены заказа
    context = {'order': order}
    # рендерим шаблон страницы подтверждения отмены заказа с полученным контекстом
    return render(request, 'cancel_order.html', context)
