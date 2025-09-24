from django.forms import ModelForm, TextInput, Textarea, ClearableFileInput, NumberInput
from .models import Event, TicketType

input_class = 'input w-full my-2'
textarea_class = 'textarea-custom w-full my-2'


class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = [
            'title',
            'description',
            'location',
            'image'
        ]

        widgets = {
            'title': TextInput(attrs={
                'class': input_class,
                'placeholder': 'Event Title'
            }),
            'description': Textarea(attrs={
                'class': textarea_class,
                'placeholder': 'Event Description...'
            }),
            'location': Textarea(attrs={
                'class': textarea_class,
                'placeholder': 'Location (Karachi, Remote)'
            }),
            'image': ClearableFileInput(attrs={
                'class': "file-input file-input-bordered my-2 h-fit w-full"
            })
        }


class TicketTypeForm(ModelForm):
    class Meta:
        model = TicketType
        fields = ['name', 'description', 'price',
                  'quantity_available']
        widgets = {
            'name': TextInput(attrs={
                'class': input_class,
                'placeholder': 'Ticket Name'
            }),
            'description': Textarea(attrs={
                'class': textarea_class,
                'placeholder': 'Ticket Description...'
            }),
            'price': NumberInput(attrs={
                'class': input_class,
                'placeholder': '$9.99',
                'steps': '0.01'
            }),
            'quantity_available': NumberInput(attrs={
                'class': input_class,
                'placeholder': '100',
                'steps': '0.01'
            }),
        }
