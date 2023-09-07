from django import forms
from users.models import Profile

class UserInfoForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'address', 'phone_number']
