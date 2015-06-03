import os, re

from django.conf import settings
from django.views.generic.base import TemplateView

from markdown import markdown


class MdCMSView(TemplateView):
    """ Render a Markdown file as HTML within a Django template. """

    template_name = "md_cms/index.html"

    def get_md_cms_file(self):
        """ 
        Determine the flat file name by the HTTP header PATH_INFO.
        If PATH_INFO is a directory, append the default file name from settings.
        """

        md_cms_file = settings.MD_CMS_ROOT + self.request.META['PATH_INFO']

        if(md_cms_file[-1:] == '/'):
            md_cms_file += settings.MD_CMS_DEFAULT_FILE

        return md_cms_file

    def get_context_data(self, **kwargs):
        context = super(MdCMSView, self).get_context_data(**kwargs)

        # Determine file name by HTTP header PATH_INFO
        md_cms_file = self.get_md_cms_file()

        if self.request.user and self.request.user.is_superuser:
            context['md_cms_edit'] = True
            context['markdown_text'] = self.request.user.get_full_name() + ': [ <a href="?edit=1">Edit Page</a> ]'
        else:
            context['markdown_text'] = ''

        try:
            # The file already exists
            with open(md_cms_file, 'r') as f:
                context['markdown_text'] += markdown(f.read())
        except:
            # The file does not exist
            if self.request.user and self.request.user.is_superuser:
                context['md_cms_edit'] = True

                if self.request.GET and self.request.GET['create']:
                    # Create the file
                    if not os.path.exists(os.path.dirname(md_cms_file)):
                        os.makedirs(os.path.dirname(md_cms_file))
                    with open(md_cms_file, "w") as f:
                        context['markdown_text'] = '# ' + re.sub(' |\/', ' ', self.request.META['PATH_INFO']).title().rstrip() + '\r\n'
                        f.write(context['markdown_text'])
                        context['markdown_text'] = markdown(context['markdown_text'])
                else:
                    # Give option to create the file
                    context['markdown_text'] = self.request.user.get_full_name() + ': No file found. [ <a href="?create=1">Create a Page</a> ]'

        return context
