from django import forms

from pagedown.widgets import PagedownWidget

class MdCMSForm(forms.Form):
    md_cms_form = forms.CharField(
        widget=PagedownWidget(),
        initial='# Insert initial content here\n\n**Testing**\n\n    class CodeBlockTest():\n        def __init__():\n            pass\n',
    )
