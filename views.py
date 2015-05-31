from django.conf import settings
from django.views.generic.base import TemplateView

from markdown import markdown


class MdCMSView(TemplateView):
    """ Render a Markdown file as HTML within a Django template. """

    template_name = "md_cms/index.html"

    def get_context_data(self, **kwargs):
        context = super(MdCMSView, self).get_context_data(**kwargs)

        md_cms_file = settings.MD_CMS_ROOT + self.request.META['PATH_INFO']
        if(md_cms_file[-1:] == '/'):
            md_cms_file += settings.MD_CMS_DEFAULT_FILE

        if self.request.user and self.request.user.is_superuser:
            context['md_cms_edit'] = True
            context['markdown_text'] = self.request.user.get_full_name() + ': [ <a href="?edit">Edit Page</a> ]'
        else:
            context['markdown_text'] = ''

        try:
            with open(md_cms_file, 'r') as f:
                context['markdown_text'] += markdown(f.read())
        except:
            if self.request.user and self.request.user.is_superuser:
                context['md_cms_edit'] = True
                context['markdown_text'] = self.request.user.get_full_name() + ': No file found. [ <a href="?create">Create a Page</a> ]'

        return context
