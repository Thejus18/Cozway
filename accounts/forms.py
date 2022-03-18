from django import forms
from .models import Account


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

   









