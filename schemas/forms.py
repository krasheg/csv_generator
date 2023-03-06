from django import forms
from .models import Schema, Column

ColumnFormSet = forms.inlineformset_factory(Schema, Column,
                                            fields=('name', 'column_type', 'order', 'range_from', 'range_to'),
                                            labels={'name': 'Name', 'column_type': 'Type',
                                                    'order': 'Order', 'range_from': 'From', 'range_to': 'To'},
                                            widgets={
                                                "column_type": forms.Select(attrs={'onchange': 'hide_range(this.id)'}),
                                            },
                                            can_delete=False,
                                            can_delete_extra=True, extra=1)


class ColumnForm(forms.ModelForm):
    class Meta:
        model = Column
        fields = ('name', 'column_type', 'range_from', 'range_to', 'order')
