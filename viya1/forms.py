from django import forms
from viya1.models import ClientDocuments  # models.py


class ClientDocumentsForm(forms.ModelForm):
    class Meta:
        model = ClientDocuments
        fields = ['name_of_document', 'description', 'date_of_upload', 'client_dokument']
        # fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(ClientDocumentsForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            # field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['class'] = 'w-100 h-100 bg-transparent border-0'