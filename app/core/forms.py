from django import forms
from .models import ServiceRequest
class RequestForm(forms.ModelForm):
    class Meta:
        model=ServiceRequest
        fields=["title","client","description","priority","due"]
        widgets={"due":forms.DateInput(attrs={"type":"date"}),"description":forms.Textarea(attrs={"rows":4})}
class TransitionForm(forms.Form):
    action=forms.ChoiceField(choices=[("active","Start work"),("review","Request approval"),("done","Approve and complete"),("reopen","Return to work"),("note","Add note")])
    note=forms.CharField(max_length=1500,required=False,widget=forms.Textarea(attrs={"rows":3}))
