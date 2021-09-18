from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, fields
from myapp.models import MyTasks
from django import forms
from django.contrib.auth.models import User

class TasksForm(ModelForm):
    """
    Form for list of tasks.
    """
    class Meta:
        model = MyTasks
        fields = ['task_title', 'task_desc', 'taskTime', 'taskDate']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["taskTime"].widget = TimeInput()
        self.fields["taskDate"].widget = DateInput()


class DateInput(forms.DateInput):
    input_type = "date"

    def __init__(self, **kwargs):
        kwargs["format"] = "%Y-%m-%d"
        super().__init__(**kwargs)

class TimeInput(forms.TimeInput):
    input_type="time"


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1','password2']