from django import forms
from academies.models import Academy

class AcademyForm(forms.ModelForm):
    class Meta:
        model = Academy

        fields = ("name", "city", "founded_year", "contact_email")

        help_texts = {
            "founded_year": "Use a value between 1800 and 2026.",
        }

        error_messages = {
            "name": {
                "required": "Please enter the academy name.",
            },

            "contact_email": {
                "invalid": "Please enter a valid email address.",
            },

            'founded_year' : {"invalid": "Please enter a valid year between 1800 and 2026."

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


