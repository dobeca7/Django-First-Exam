from django import forms

from scouting.models import ScoutReport, Skill


class ScoutReportForm(forms.ModelForm):
    class Meta:
        model = ScoutReport
        exclude = ["created_at", "updated_at"]

        help_texts = {
            "skills": "Optional. Choose one or more skills.",
        }

        widgets = {
            "rating": forms.NumberInput(attrs={'placeholder': "Use a value between 1 to 10",}),
            "skills": forms.CheckboxSelectMultiple(),
            "notes": forms.Textarea(attrs={"rows": 4, "placeholder": "Short scouting notes..."}),
        }

    skills = forms.ModelMultipleChoiceField(
        queryset=Skill.objects.none(),
        required=False,
        widget=forms.CheckboxSelectMultiple(),
        help_text="Optional. Choose one or more skills.",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["skills"].queryset = Skill.objects.order_by("name")

    def clean(self):
        cleaned_data = super().clean()
        recommendation = cleaned_data.get("recommendation")
        rating = cleaned_data.get("rating")

        if recommendation == "sign" and rating is not None and rating < 7:
            self.add_error("recommendation", "Use 'Sign' only for ratings over 7.")

        return cleaned_data

