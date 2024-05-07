from django import forms
from .models import Reservation


class ReserveTableForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ('name', 'email', 'phone', 'number_of_persons', 'date', 'time')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'id': 'name', 'placeholder': 'Ваше ім\'я',
                                           'data-rule': 'minlen:1'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Ваш email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'id': 'email',
                                            'placeholder': 'Ваш номер телелфону', 'data-rule': 'email'}),
            'number_of_persons': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Кількість осіб'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Дата бронювання'}),
            'time': forms.TimeInput(attrs={'class': 'form-control', 'placeholder': 'Час бронювання'}),
        }
        help_texts = {
            'phone': 'Введіть номер телефону у форматі 380*********',
            'date': 'Введіть дату у форматі YYYY-MM-DD',
        }
        error_messages = {
            'name': {
                'required': 'Це поле є обов\'язковим',
            },
            'email': {
                'required': 'Це поле є обов\'язковим',
            },
            'phone': {
                'required': 'Це поле є обов\'язковим',
            },
            'number_of_persons': {
                'required': 'Це поле є обов\'язковим',
            },
            'date': {
                'required': 'Це поле є обов\'язковим',
            },
            'time': {
                'required': 'Це поле є обов\'язковим',
            },
        }
