from django import forms
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
import io
from .models import Order, OrderStatus , PickupPoint

class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = '__all__'
        widgets = {
            'order_number': forms.TextInput(attrs={'class': 'form-control'}),
            'order_date':forms.DateInput(attrs={'class': 'form-control'}),
            'delivery_date':forms.DateInput(attrs={'class': 'form-control'}),
            'customer_id':forms.TextInput(attrs={'class': 'form-control'}),
            'pickup_point_id':forms.TextInput(attrs={'class': 'form-control'}),
            'status':forms.TextInput(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

        if 'order_number' in self.fields:
            self.fields['order_number'].help_text = 'Уникальный номер заказа'
        
        if 'order_date' in self.fields:
            self.fields['order_date'].help_text = 'Дата оформления заказа'
            
        if 'delivery_date' in self.fields:
            self.fields['delivery_date'].help_text = 'Ожидаемая дата доставки'

        if 'customer_id' in self.fields:
            self.fields['customer_id'].help_text = 'ID клиента'

        if 'pickup_point_id' in self.fields:
            self.fields['pickup_point_id'].help_text = 'ID пункта выдачи'

        if 'status' in self.fields:
            self.fields['status'].help_text = 'Текущий статус (например, Новый или Завершен)'
        

