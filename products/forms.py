from django import forms
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
import io
from .models import PickupPoint, Product, Order


class ProductForm(forms.ModelForm):
    """Форма для создания/редактирования товара"""

    class Meta:
        model = Product
        fields = [
            'name', 'category', 'description', 'manufacturer',
            'supplier', 'price', 'unit', 'quantity', 'discount', 'image'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'manufacturer': forms.Select(attrs={'class': 'form-control'}),
            'supplier': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'unit': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'discount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['price'].help_text = 'Цена в рублях'
        self.fields['discount'].help_text = 'Скидка в процентах (0-100)'
        self.fields['quantity'].help_text = 'Количество на складе (не может быть отрицательным)'
        self.fields['image'].help_text = 'Изображение товара (опционально, не больше 300x200)'

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if not image:
            return image

        uploaded_image = Image.open(image)
        max_width = 300
        max_height = 200

        if uploaded_image.width <= max_width and uploaded_image.height <= max_height:
            image.seek(0)
            return image

        uploaded_image.thumbnail((max_width, max_height))
        buffer = io.BytesIO()
        image_format = uploaded_image.format or 'PNG'
        uploaded_image.save(buffer, format=image_format)
        buffer.seek(0)

        return InMemoryUploadedFile(
            file=buffer,
            field_name='image',
            name=image.name,
            content_type=image.content_type,
            size=buffer.getbuffer().nbytes,
            charset=None,
        )
    
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
        

