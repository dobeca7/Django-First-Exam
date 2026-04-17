from django import forms
from django.utils import timezone

from academies.models import Academy
from matches.models import Match, MatchParticipation
from players.models import Player


class MatchForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = (
            "home_academy",
            "away_academy",
            "date",
            "location",
            "competition",
            "home_score",
            "away_score",
            "notes",
        )
        labels = {
            "date": "Match date",
            "home_score": "Home score",
            "away_score": "Away score",
        }
        help_texts = {
            "competition": "Optional. Example: Elite Youth League.",
            "notes": "Optional short match context.",
        }
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "location": forms.TextInput(attrs={"placeholder": "Example: Sofia Training Base"}),
            "competition": forms.TextInput(attrs={"placeholder": "Example: U17 League"}),
            "home_score": forms.NumberInput(attrs={"min": 0}),
            "away_score": forms.NumberInput(attrs={"min": 0}),
            "notes": forms.Textarea(attrs={"rows": 4, "placeholder": "Pitch conditions, match notes, standout moments..."}),
        }
        error_messages = {
            "home_academy": {"required": "Please choose the home academy."},
            "away_academy": {"required": "Please choose the away academy."},
            "location": {"required": "Please enter the match location."},
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        self._user = user
        self.fields["date"].input_formats = ["%Y-%m-%d"]

        if user and not user.is_superuser:
            self.fields["home_academy"].queryset = Academy.objects.order_by("name")
            self.fields["away_academy"].queryset = Academy.objects.order_by("name")
            self.fields["home_academy"].help_text = "Choose one of your academies or another academy as the home side."
            self.fields["away_academy"].help_text = "Choose one of your academies or another academy as the away side."

    def clean_date(self):
        match_date = self.cleaned_data.get("date")
        if match_date and match_date > timezone.localdate():
            raise forms.ValidationError("Please choose today or a past match date.")
        return match_date

    def clean(self):
        cleaned_data = super().clean()
        home_academy = cleaned_data.get("home_academy")
        away_academy = cleaned_data.get("away_academy")

        if home_academy and away_academy and home_academy == away_academy:
            self.add_error("away_academy", "The away academy must be different from the home academy.")

        user = getattr(self, "_user", None)
        if user and not user.is_superuser:
            owned_ids = set(user.owned_academies.values_list("id", flat=True))
            selected_ids = {academy.id for academy in (home_academy, away_academy) if academy}
            if selected_ids and not (selected_ids & owned_ids):
                error_message = "One of the two academies must be your own academy."
                self.add_error("home_academy", error_message)
                self.add_error("away_academy", error_message)

        return cleaned_data

class MatchParticipationForm(forms.ModelForm):
    class Meta:
        model = MatchParticipation
        fields = ("player", "started", "minutes_played", "goals", "assists")
        labels = {
            "started": "Starting lineup",
            "minutes_played": "Minutes played",
        }
        help_texts = {
            "minutes_played": "Use a value between 0 and 120.",
        }
        widgets = {
            "minutes_played": forms.NumberInput(attrs={"min": 0, "max": 120}),
            "goals": forms.NumberInput(attrs={"min": 0}),
            "assists": forms.NumberInput(attrs={"min": 0}),
        }

    def __init__(self, *args, **kwargs):
        self.match = kwargs.pop("match")
        super().__init__(*args, **kwargs)
        self.fields["player"].queryset = Player.objects.filter(
            academy_id__in=[self.match.home_academy_id, self.match.away_academy_id]
        ).order_by("name")
