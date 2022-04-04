from django import forms
from .models import Account
from.models import UserProfile


class RegistertionForm(forms.ModelForm):
    password= forms.CharField(widget=forms.PasswordInput(attrs={

        'placeholder': 'Enter Password',
        'class': 'form-control',
    }))
    Confirm_password= forms.CharField(widget=forms.PasswordInput(attrs={

        'placeholder': 'Confirm Password',
        'class': 'form-control',
    }))
    
    class Meta:
        model = Account
        fields= ['first_name','last_name','phone_number','email','password']

    def clean(self):
        cleaned_data = super(RegistertionForm, self).clean()
        password = cleaned_data.get('password')
        Confirm_password = cleaned_data.get('Confirm_password')


        if password != Confirm_password:
            raise forms.ValidationError(
                    "Password does not match!! "
            )
   

    def __init__(self, *args, **kwargs):
        super(RegistertionForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder']= 'Enter First Name'
        self.fields['last_name'].widget.attrs['placeholder']= 'Enter Last Name'
        self.fields['email'].widget.attrs['placeholder']= 'Enter the Email address'
        self.fields['phone_number'].widget.attrs['placeholder']= 'Enter the Phone Number'

        for field in self.fields:
            self.fields[field].widget.attrs['class']= 'form-control'

   
class UserForm(forms.ModelForm):
    class Meta:
        model = Account
        fields =('first_name','last_name','phone_number')

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class']= 'form-control'


class UserProfileForm(forms.ModelForm):
    profile_picture= forms.ImageField(required=False,error_messages={'invalid' :("Image files only")}, widget=forms.FileInput)  #for removing the currently set profile picture path
    class Meta:
        model=UserProfile
        fields = ('address_line_1', 'address_line_2', 'city', 'state', 'country', 'profile_picture')


    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class']= 'form-control'







