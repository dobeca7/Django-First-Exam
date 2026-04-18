from datetime import date

from django import forms

from players.models import Player


class PlayerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        if user and not user.is_superuser:
            self.fields["academy"].queryset = user.owned_academies.order_by("name")

    birth_date = forms.DateField(
        input_formats=["%Y-%m-%d"],
        help_text="Use format YYYY-MM-DD.",
    )

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
            "birth_date": forms.DateInput(
                format="%Y-%m-%d",
                attrs={"type": "date"},
            ),
            "height": forms.NumberInput(attrs={"placeholder": "Example: 178"}),
            "weight": forms.NumberInput(attrs={"placeholder": "Example: 72"}),
            "potential": forms.NumberInput(attrs={"placeholder": "Example: 84", "min": 1, "max": 100}),
        }

    def clean_height(self):
        height = self.cleaned_data.get("height")
        if height is None:
            return height
        if not (1 <= height <= 300):
            raise forms.ValidationError("Height must be between 1 and 300 cm.")
        return height

    def clean_weight(self):
        weight = self.cleaned_data.get("weight")
        if weight is None:
            return weight
        if not (1 <= weight <= 200):
            raise forms.ValidationError("Weight must be between 1 and 200 kg.")
        return weight


class PlayerDeleteForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = (
            "name",
            "academy",
            "position",
            "potential",
        )
        labels = {
            "potential": "Potential (1-100)",
        }
        help_texts = {
            "academy": "Read-only academy assignment for confirmation before deletion.",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.disabled = True
