from django import forms

# template (https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Forms)
class templateForm(forms.Form):
    dummyText = forms.CharField(help_text="Enter text")



