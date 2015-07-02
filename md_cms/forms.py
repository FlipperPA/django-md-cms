from django import forms

from pagedown.widgets import PagedownWidget

class MdCMSForm(forms.Form):
    md_cms_textarea = forms.CharField(
        widget=PagedownWidget(),
    )
