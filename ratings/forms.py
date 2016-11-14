from django import forms
from django.forms import ModelForm
from ratings.models import Review

class SearchForm(forms.Form):
    searchstring = forms.CharField(label='Search', max_length=100)


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['course_id', 'user', 'overall', 'lectures', 'assignments', 'workload', 'comments']
