from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

class UserCreateForm(UserCreationForm):

    class Meta():
        fields = ('username', 'email', 'password1', 'password2') #Fields user can access
        model = get_user_model()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #We can set the label for a form here instead of html if we want:
        self.fields['username'].label = 'Display Name'
        self.fields['email'].label = 'Email Address'
