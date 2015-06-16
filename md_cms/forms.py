from django import forms

from pagedown.widgets import PagedownWidget

#from md_cms.views import MdCMSView

class MdCMSForm(forms.Form):
    md_cms_form = forms.CharField(
        widget=PagedownWidget(),
        initial='ASDF ASDF ASDF',
    )
