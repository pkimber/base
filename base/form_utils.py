from bleach import (
    clean,
    ALLOWED_TAGS,
    ALLOWED_ATTRIBUTES,
)

from django import forms


def bleach_clean(data):
    """Use bleach to clean up html."""
    attributes = ALLOWED_ATTRIBUTES
    styles = []
    tags = ALLOWED_TAGS + [u'br', u'p',]
    return clean(data, tags=tags, attributes=attributes, styles=styles)


class RequiredFieldForm(forms.ModelForm):
    """Add the 'required' attribute"""

    def __init__(self, *args, **kwargs):
        super(RequiredFieldForm, self).__init__(*args, **kwargs)
        for name in self.fields:
            if self.fields[name].required:
                self.fields[name].widget.attrs.update({
                    'required': None,
                    'placeholder': 'This is a required field',
                })
