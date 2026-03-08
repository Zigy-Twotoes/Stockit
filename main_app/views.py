from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from main_app.models import Product, OrderGuide, OrderList
from django.forms import inlineformset_factory
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import OrderListItemForm
from datetime import date


# Create your views here.
def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user= form.save()
            login(request, user)
            return redirect('products-list')
        else:
            error_message = 'Invalid sign up - try again'
    else:
        form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'signup.html', context)

# Class views


class Home(LoginView):
    template_name = 'home.html'

class ProductListView(ListView):
    model = Product
    template_name = 'inventory/products-list.html'

class ProductCreateView(CreateView):
    model = Product
    fields = ['name', 'par']
    template_name = 'inventory/products-form.html'
    success_url = reverse_lazy('products-list')

class ProductUpdateView(UpdateView):
    model = Product
    fields = ['name', 'par']
    template_name = 'inventory/products-form.html'
    success_url = reverse_lazy('products-list') 

class ProductDetailView(DetailView):
    model = Product
    template_name = 'inventory/products-details.html'

class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'inventory/products-confirm-delete.html'
    success_url = reverse_lazy('products-list')

# Order Guide views
OrderListForm = inlineformset_factory(
    OrderGuide,
    OrderList,
    form=OrderListItemForm, 
    fields=('product', 'stock_on_hand', 'par_level', 'quantity_ordered' ),
    extra=1,
    can_delete=False
    )

class OrderHistoryListView(LoginRequiredMixin, ListView):
    model = OrderGuide
    template_name = 'orders/orders-history.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return OrderGuide.objects.filter(user=self.request.user).order_by('-id')
    
class OrderDetailView(LoginRequiredMixin, DetailView):
    model = OrderGuide
    template_name = 'orders/orders-details.html'
    context_object_name = 'order'

class OrderGuideCreateView(CreateView):
    model = OrderGuide
    fields = ['name']
    template_name = 'orders/orders-create.html'
    success_url = reverse_lazy('orders-history')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_update'] = False
        context['date'] = date.today()
        if self.request.method == 'POST':
            context['order_items'] = OrderListForm(self.request.POST)
        else:
            products = Product.objects.all()
            initial_data = [{'product': p.id} for p in products]
            formset = OrderListForm(queryset=OrderList.objects.none(), initial=initial_data)
            formset.extra = len(products)
            context['order_items'] = formset
        return context
    
    def form_valid(self, form):
        form_data = self.get_context_data()
        order_items = form_data['order_items']
        form.instance.user = self.request.user

        if form.is_valid() and order_items.is_valid():
            self.object = form.save()
            order_items.instance = self.object
            order_items.save()
            return super().form_valid(form)
        else:
            return self.render_to_response(context)


class OrderGuideUpdateView(UpdateView):
    model = OrderGuide
    fields = ['name']
    template_name = 'orders/orders-create.html'
    success_url = reverse_lazy('orders-history') 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_update'] = True
        if self.request.method == 'POST':
            context['order_items'] = OrderListForm(self.request.POST, instance=self.object)
        else:
            context['order_items'] = OrderListForm(instance=self.object)
            for form in context['order_items']:
                if form.instance.pk:
                    form.product_obj = form.instance.product
        return context
    
    def form_valid(self, form):
        context = self.get_context_data() 
        order_items = context['order_items']
        if form.is_valid() and order_items.is_valid():
            self.object = form.save()
            order_items.instance = self.object
            order_items.save()
            return super().form_valid(form)
        return self.render_to_response(context)
    
class OrderDeleteView(LoginRequiredMixin, DeleteView):
    model = OrderGuide
    success_url = reverse_lazy('orders-history')
    template_name = 'orders/orders-confirm-delete.html'
    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)