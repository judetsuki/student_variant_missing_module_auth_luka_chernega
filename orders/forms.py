from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'
        widgets = {
            'order_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'delivery_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'pickup_point_id': forms.Select(attrs={'class': 'form-control'}),
            'customer_id': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

        help_texts = {
            'order_number': 'Уникальный номер заказа',
            'order_date': 'Дата оформления заказа',
            'delivery_date': 'Ожидаемая дата доставки',
            'customer': 'Выберите клиента',
            'pickup_point': 'Выберите пункт выдачи',
            'status': 'Текущий статус заказа',
        }
        
        for field, text in help_texts.items():
            if field in self.fields:
                self.fields[field].help_text = text
