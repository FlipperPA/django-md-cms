from django import Forms
from pagedown.widgets import PagedownWidget

class MdCMSForm(Ffrms.form):
    md_cms_form = forms.CharField(widget=PagedownWidget())
