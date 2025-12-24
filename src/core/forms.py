from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column


def get_dynamic_crispy_form(
        model,
        fields='__all__',
        exclude=None,  # <--- New parameter
        widgets=None,
        placeholders=None,
        column_classes=None,
        empty_labels=None,
        enable_help_texts=True,  # <---- Keep this feature
        form_class='row g-3',
        label_class='form-label'
):
    model_name = model._meta.verbose_name.title()
    widgets = widgets or {}
    exclude = exclude or []  # Default empty list

    class BaseDynamicForm(forms.ModelForm):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            for field_name, field in self.fields.items():
                verbose_field = field_name.replace("_", " ")

                # --- Enable or disable help texts ---
                if enable_help_texts:
                    field.help_text = field.help_text or ''
                else:
                    field.help_text = ''

                # --- Placeholder ---
                if isinstance(field.widget, (forms.TextInput, forms.Textarea)):
                    placeholder = (
                        placeholders[field_name]
                        if placeholders and field_name in placeholders
                        else f"Enter {model_name} {verbose_field}"
                    )
                    field.widget.attrs['placeholder'] = placeholder

                # --- Empty label for ChoiceFields ---
                if hasattr(field, 'empty_label') and field.empty_label is not None:
                    field.empty_label = (
                        empty_labels[field_name]
                        if empty_labels and field_name in empty_labels
                        else f"Select {model_name} {verbose_field}"
                    )

                # --- DateTime Fields ---
                if isinstance(field, forms.DateTimeField) or isinstance(field.widget, forms.DateTimeInput):
                    field.widget = forms.DateTimeInput(attrs={'type': 'datetime-local'})

                if isinstance(field, forms.DateField) or isinstance(field.widget, forms.DateInput):
                    field.widget = forms.DateTimeInput(attrs={'type': 'date'})

            # Crispy helper
            self.helper = FormHelper()
            self.helper.form_class = form_class
            self.helper.label_class = label_class
            self.helper.layout = Layout(
                Row(
                    *[
                        Column(field_name,
                               css_class=column_classes.get(field_name, 'col-md-12') if column_classes else 'col-md-12')
                        for field_name in self.fields
                    ]
                )
            )

    Meta = type('Meta', (), {
        'model': model,
        'fields': fields,
        'exclude': exclude,  # <--- Add exclude here
        'widgets': widgets,
    })

    return type(f'{model.__name__}DynamicForm', (BaseDynamicForm,), {'Meta': Meta})