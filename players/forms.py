from datetime import date

from django import forms

from players.models import Player


class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = '__all__'
        labels = {
            "height": "Height (cm)",
            "weight": "Weight (kg)",
            "potential": "Potential (1-100)",
        }
        help_texts = {
            "potential": "Use a value between 1 and 100.",
        }
        error_messages = {
            "name": {
                "required": "Please enter the player name.",
            },
            "academy": {
                "required": "Please select an academy.",
            },
        }
        widgets = {
            'birth_date': forms.DateInput(format="%d-%m-%Y", attrs={"type": "date"}),
            "height": forms.NumberInput(attrs={"placeholder": "Example: 178"}),
            "weight": forms.NumberInput(attrs={"placeholder": "Example: 72"}),
            "potential": forms.NumberInput(attrs={"placeholder": "Example: 84", "min": 1, "max": 100}),
        }

