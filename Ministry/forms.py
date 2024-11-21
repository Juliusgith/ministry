from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'address', 'comment_text']  # Correct
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Address (optional)'}),
            'comment_text': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your Comment'}),
        }



from django import forms
from .models import ContactSubmission

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactSubmission
        fields = ['name', 'email', 'phone', 'address', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }


from django import forms
from .models import Donation

class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ['name', 'phone', 'email', 'country', 'district', 'subcounty', 'parish', 'village', 'item_category', 'amount']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'item_category': forms.Select(attrs={'class': 'form-control', 'id': 'id_item_category'}),
        }


    def __init__(self, *args, **kwargs):
        super(DonationForm, self).__init__(*args, **kwargs)
        
        # Display a warning message based on the country entered by the user
        country = self.initial.get('country', '')
        if country:
            if country.lower() == 'uganda':
                self.fields['amount'].help_text = "Please enter the amount in Ugandan Shillings."
            elif country.lower() == 'united states':
                self.fields['amount'].help_text = "Please enter the amount in US Dollars."
            else:
                self.fields['amount'].help_text = "Please enter the amount based on your currency."
        else:
            self.fields['amount'].help_text = "Please enter the amount based on your currency."





from django import forms

class EmailForm(forms.Form):
    email = forms.EmailField(label='Enter your email')

class PasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput, label='Enter the password')

class UploadForm(forms.Form):
    form_file = forms.FileField(label='Upload your form')
