from django.views.generic.base import TemplateView

from markdown import markdown

class MdCMSView(TemplateView):
    """ Render a Markdown file as HTML within a Django template. """


    template_name = "md_cms/index.html"

    def get_context_data(self, **kwargs):
        context = super(MdCMSView, self).get_context_data(**kwargs)

        with open('/vagrant/html/markdown_cms/md_cms/README.md', 'r') as f:
            context['markdown_text'] = markdown(f.read())

        return context
