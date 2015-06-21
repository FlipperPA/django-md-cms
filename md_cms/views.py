import os, re

from django.conf import settings
from django.http import Http404, HttpResponse
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from markdown import markdown
from md_cms.forms import MdCMSForm

from pprint import pprint

class MdCMSEdit(FormView):
    """
    Create or Update and existing page using the Pagedown editor.
    """

    template_name = 'edit.html'
    form_class = MdCMSForm

    def __init__(self):
        pass

    def get(self, request, *args, **kwargs):
        m = MdCMSView()
        md_cms_file = m.get_md_cms_file(self.request.META['PATH_INFO'])
        print(md_cms_file + 'YYY')
        # See get_md_cms_file to see why returning just first four characters of md_cms_file
        return HttpResponse(md_cms_file)

    def form_valid(self, form):
        """
        FORM is valid, given the definition.
        Write the file,  and return an HttpResponse.
        """

        # Write file here

        return super(MdCMSView, self).form_valid(form)


class MdCMSView(TemplateView):
    """ Render a Markdown file as HTML within a Django template. """

    template_name = "index.html"

    def __init__(self):
        pass

    def get_md_cms_file(self, path_info = None):
        """ 
        Determine the flat file name by the HTTP header PATH_INFO.
        If PATH_INFO is a directory, append the default file name from settings.
        """

        if path_info is None:
            path_info = self.request.META['PATH_INFO']

        md_cms_file = settings.MD_CMS_ROOT + path_info

        print(md_cms_file + 'ZZZ')
        if(md_cms_file.endswith(settings.MD_CMS_EDIT_SUFFIX)):
            md_cms_file = md_cms_file[:len(settings.MD_CMS_EDIT_SUFFIX)]
        print(md_cms_file + 'ZZZ')

        if(md_cms_file[-1:] == '/'):
            md_cms_file += settings.MD_CMS_DEFAULT_FILE

        return md_cms_file

    def get_md_cms_file_content(self, md_cms_file):
        try:
            # The file already exists
            with open(md_cms_file, 'r') as f:
                return markdown(f.read())
        except:
            # The file does not exist
            return False

    def create_md_cms_file(self, md_cms_file):
        """
        Create the appropriate directories if necessary given the md_cms_file path, and
        create the new file with expanding PATH_INFO as a H1.
        """

        if not os.path.exists(os.path.dirname(md_cms_file)):
            os.makedirs(os.path.dirname(md_cms_file))

        markdown_text = '# ' + re.sub(' |\/', ' ', self.request.META['PATH_INFO']).title().rstrip() + '\r\n'

        with open(md_cms_file, "w") as f:
            f.write(markdown_text)

        return markdown(markdown_text)

    def get_context_data(self, **kwargs):
        context = super(MdCMSView, self).get_context_data(**kwargs)

        # Determine file name by HTTP header PATH_INFO
        md_cms_file = self.get_md_cms_file()

        if self.request.user and self.request.user.is_superuser:
            context['md_cms_edit'] = True
            context['md_cms_edit_suffix'] = settings.MD_CMS_EDIT_SUFFIX

        try:
            # Get the content from the filesystem
            context['markdown_text'] = self.get_md_cms_file_content(md_cms_file)
        except:
            # The file does not exist
            if self.request.user and self.request.user.is_superuser:
                context['md_cms_edit'] = True

                if self.request.GET and self.request.GET['edit']:
                    # Create the file
                    context['markdown_text'] = create_md_cms_file(md_cms_file)
            else:
                raise Http404('Sorry, the requested page was not found.')

        return context
