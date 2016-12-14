from django import forms
from django.forms import ModelForm
from ratings.models import Review
from django.contrib.auth.forms import UserCreationForm

class SearchForm(forms.Form):
    searchstring = forms.CharField(label='Search', max_length=100)

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['course_id', 'user', 'overall', 'lectures', 'assignments', 'workload', 'comments']

class UserCreateForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        
        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None