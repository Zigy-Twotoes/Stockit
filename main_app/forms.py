from django import forms
from main_app.models import OrderList, Product

class OrderListItemForm(forms.ModelForm):
    class Meta:
        model = OrderList
        fields = ('product', 'stock_on_hand', 'par_level', 'quantity_ordered')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.product_obj = None  
        product_id = self.initial.get('product')
        if not product_id and self.data:
            field_name = f"{self.prefix}-product"
            product_id = self.data.get(field_name)

        if product_id:
            try:
                self.product_obj = Product.objects.get(id=product_id)
            except (Product.DoesNotExist, ValueError):
                pass

        if not self.product_obj and self.instance.pk:
            try:
                self.product_obj = self.instance.product
            except OrderList.product.RelatedObjectDoesNotExist:
                pass