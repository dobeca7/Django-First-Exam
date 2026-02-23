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


class AcademyDeleteForm(forms.ModelForm):
    class Meta:
        model = Academy
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.disabled = True


