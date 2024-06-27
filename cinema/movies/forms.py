from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import *


class SearchForm(forms.Form):
    helper = FormHelper()
    helper.form_id = "search_crispy_form"
    helper.form_method = "POST"
    helper.add_input(Submit("submit", "Search"))
    search_string = forms.CharField(label="Search for movies", max_length=200, min_length=3, required=True)
    CHOICES = [("Title", "Search by title"), ("Director", "Search by director"), ("Tags", "Search by tags")]
    search_where = forms.ChoiceField(label="Where", required=True, choices=CHOICES)
    sort_by_score = forms.BooleanField(label="Sort by score", required=False)