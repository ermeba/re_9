from django import forms
from viya1.models import ClientDocuments  # models.py


class ClientDocumentsForm(forms.ModelForm):
    class Meta:
        model = ClientDocuments
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(ClientDocumentsForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'