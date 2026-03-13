from datetime import date
from django import forms
from academies.models import Academy

class AcademyForm(forms.ModelForm):
    class Meta:
        model = Academy

        fields = ("name", "city", "founded_year", "contact_email")

        error_messages = {
            "name": {
                "required": "Please enter the academy name.",
            },

            "contact_email": {
                "invalid": "Please enter a valid email address.",
            },

        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        current_year = date.today().year
        self.fields["founded_year"].help_text = f"Use a value between 1800 and {current_year}."
        self.fields["founded_year"].error_messages["invalid"] = (
            f"Please enter a valid year between 1800 and {current_year}."
        )

    def clean_founded_year(self):
        founded_year = self.cleaned_data.get("founded_year")
        current_year = date.today().year
        if founded_year and founded_year > current_year:
            raise forms.ValidationError(f"Use a value between 1800 and {current_year}.")
        return founded_year


class AcademyDeleteForm(forms.ModelForm):
    class Meta:
        model = Academy
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.disabled = True
