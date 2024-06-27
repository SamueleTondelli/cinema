from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
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
    
    
class ReservationForm(forms.Form):
    helper = FormHelper()
    helper.form_id = "create_reservation_crispy_form"
    helper.form_method = "POST"
    helper.add_input(Submit("submit","Make Reservation"))
    
    def __init__(self, screening_id, *args, **kwargs):
        super().__init__(args, kwargs)
        s = get_object_or_404(MovieScreening, pk=screening_id)
    
    class Meta:
        model = Reservation
        fields = ["seats"]