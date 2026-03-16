from django import template

register = template.Library()

@register.simple_tag
def stars(player):
    avg_rating = getattr(player, "avg_report_rating", None)
    if avg_rating is None:
        return ""

    rounded_rating = max(int(avg_rating), 0)
    return "*" * rounded_rating
