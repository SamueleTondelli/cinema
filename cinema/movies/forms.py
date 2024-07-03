from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import *
from django.forms.widgets import *
import json


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

        
class AddMovieForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_id = "addmovie_crispy_form"
    helper.form_method = "POST"
    helper.add_input(Submit("submit", "Add Movie"))
    actor_list = forms.CharField(label="Actors", max_length=200, min_length=3, required=True)
    
    class Meta:
        model = Movie
        fields = ["title", "director", "duration", "tags", "cover"]
        widgets = {
            "tags": CheckboxSelectMultiple(),
        }
        
    def save(self, commit=True):
        m = super().save(commit)
        m.actors = self.cleaned_data.get("actor_list").split(",")
        if commit:
            m.save()
        return m

    
class AddScreeningForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_id = "addscreening_crispy_form"
    helper._form_method = "POST"
    helper.add_input(Submit("submit", "Add Screening"))
    
    class Meta:
        model = MovieScreening
        fields = ["movie", "room", "date"]
        widgets = {
            "date": DateTimeInput(format='%d/%m/%Y %H:%M', attrs={'type': 'datetime-local'})
        }
        
    def save(self, commit=True):
        s = super().save(commit)
        s.init_seats()
        if commit:
            s.save()
        return s
    
    
class AddRoomForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_id = "addroom_crispy_form"
    helper.form_method = "POST"
    helper.add_input(Submit("submit", "Add Room"))
    
    class Meta:
        model = CinemaRoom
        fields = "__all__" 
        labels = {
            "seat_rows": "Number of rows",
            "seat_cols": "Number of seats per row"
        }
        widgets = {
            "seat_rows": NumberInput(attrs={"min": 1, "max": 26}),
            "seat_cols": NumberInput(attrs={"min": 1, "max": 50})
        }