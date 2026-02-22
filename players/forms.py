from datetime import date

from django import forms

from players.models import Player


class BasePlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = '__all__'
        labels = {
            "name": "Player name",
            "birth_date": "Birth date",
            "age": "Age",
            "position": "Position",
            "dominant_foot": "Dominant foot",
            "potential": "Potential",
            "academy": "Academy",
            "skills": "Skills",
        }
        help_texts = {
            "potential": "Value between 1 and 100.",
            "skills": "Optional. You can select multiple.",
        }
        widgets = {
            "age":forms.NumberInput(attrs={"placeholder": "Age"}),
            "potential": forms.NumberInput(attrs={"min": 1, "max": 100}),
            "skills": forms.SelectMultiple(attrs={"size": 6}),
        }

class PlayerCreateForm(BasePlayerForm):
    pass


class PlayerEditForm(BasePlayerForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["academy"].disabled = True
        self.fields["academy"].help_text = "Academy is read-only in edit mode."
