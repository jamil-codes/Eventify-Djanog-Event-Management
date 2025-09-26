from django.forms import ModelForm, TextInput, Textarea, ClearableFileInput, NumberInput, DateTimeInput
from django.utils import timezone
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
            'image',
            'start_time',
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
            }),
            'start_time': DateTimeInput(
                attrs={
                    'class': input_class,
                    'type': 'datetime-local',
                },
                format='%Y-%m-%dT%H:%M'
            ),
        }


class TicketTypeForm(ModelForm):
    class Meta:
        model = TicketType
        fields = ['name', 'description', 'price', 'quantity_available']
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
                'placeholder': '9.99',
                'step': '0.01'   # fixed
            }),
            'quantity_available': NumberInput(attrs={
                'class': input_class,
                'placeholder': '100',
                'step': '1'      # fixed
            })
        }
