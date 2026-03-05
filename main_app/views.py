from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from main_app.models import Product, OrderGuide, OrderList
from django.forms import inlineformset_factory
from django.views.generic import UpdateView, CreateView

# Create your views here.
def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user= form.save()
            login(request, user)
            return redirect('order-index')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'from': form, 'error_message': error_message}
    return render(request, 'signup.html', context)

# Class views

class Home(LoginView):
    template_name = 'home.html'



# Order Guide views
OrderListForm = inlineformset_factory(
    OrderGuide,
    OrderList, 
    fields=('product', 'stock_on_hand', 'par_level'),
)

class Home(LoginView):
    template_name = 'home.html'

class OrderGuideCreateView(CreateView):
    model = OrderGuide
    fields = ['name']
    
    def get_form_data(self, **kwargs):
        data = super().get_form_data(**kwargs)
        if self.request.POST:
            data['order_items'] = OrderListForm(self.requst.POST)
        else:
            data['order_items'] = OrderListForm()
        return data
    
    def form_valid(self, form):
        form_data = self.get_form_data()
        order_items = form_data['order_items']
        form.instance.user = self.request.user

        if form.is_valid() and order_items.is_valid():
            self.object = form.save()
            order_items.instance = self.object
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_form_data(form=form))


class OrderGuideUpdateView(UpdateView):
    model = OrderGuide
    fields = ['name']
    def get_form_data(self, **kwargs):
        data = super().get_form_data(**kwargs)
        if self.request.POST:
            data['order_items'] = OrderListForm(self.request.POST, instance=self.object)
        else: 
            data['order_items'] = OrderListForm(instance=self.object)
        return data
    
    def form_valid(self, form):
        form_data = self.get_form_data()
        order_items = form_data['order_items']
        if form.is_valid() and order_items.is_valid():
            self.object = form.save()
            order_items.instance = self.object
            order_items.save()
            return super().form_valid(form)
        return self.render_to_response(self.get_form_data(form=form))