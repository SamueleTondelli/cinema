from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field, HTML, Row, Column
from .models import *
from django.shortcuts import get_object_or_404


class SearchForm(forms.Form):
    helper = FormHelper()
    helper.form_id = "search_crispy_form"
    helper.form_method = "POST"
    helper.add_input(Submit("submit", "Search"))
    search_string = forms.CharField(label="Search for movies", max_length=200, min_length=3, required=True)
    CHOICES = [("Title", "Search by title"), ("Director", "Search by director"), ("Tags", "Search by tags")]
    search_where = forms.ChoiceField(label="Where", required=True, choices=CHOICES)
    sort_by_score = forms.BooleanField(label="Sort by score", required=False)
    
    
class ReviewForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_id = "review_crispy_form"
    helper.form_method = "POST"
    score = forms.IntegerField(label="Score", max_value=10, min_value=0)
    text = forms.CharField(label="Text", widget=forms.Textarea, max_length=300)
    helper.add_input(Submit("submit", "Leave review!"))
    
    class Meta:
        model = Review
        fields = ["score", "text"]