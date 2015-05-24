from django.views.generic.base import TemplateView
from markdown import markdownFromFile

class MdCMSView(TemplateView):
    """ Render a Markdown file as HTML within a Django template. """


    template_name = "md_cms/index.html"

    def get_context_data(self, **kwargs):
#        print(**kwargs)
        context = super(MdCMSView, self).get_context_data(**kwargs)
        s = StringIO()
        markdownFromFile(input='/vagrant/html/markdown_cms/md_cms/README.md', output=s)
        context['markdown_text'] = s.getvalue()
        s.close()

        return context
