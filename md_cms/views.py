import os, re

from django.conf import settings
from django.http import Http404
from django.views.generic.edit import FormView

from markdown import markdown
from md_cms.forms import MdCMSForm

class MdCMSView(FormView):
    """ Render a Markdown file as HTML within a Django template. """

    template_name = "index.html"
    form_class = MdCMSForm
    success_url = '/'

    def form_valid(self, form):
        """
        FORM is valid, given the definition.
        Write the file,  and return an HttpResponse.
        """

        # Write file here

        return super(MdCMSView, self).form_valid(form)

    # Populate initial data from flatfile
    def get_initial(self):
        pass
#        return {
#            'md_cms_form': self.md_cms_file
#        }

    def get_md_cms_file(self):
        """ 
        Determine the flat file name by the HTTP header PATH_INFO.
        If PATH_INFO is a directory, append the default file name from settings.
        """

        md_cms_file = settings.MD_CMS_ROOT + self.request.META['PATH_INFO']

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
        print('XXXXXXXXXXXXXXXXX')
        if self.request.user and self.request.user.is_superuser:
            context['md_cms_edit'] = True
            context['md_cms_edit_suffix'] = settings.MD_CMS_EDIT_SUFFIX

            # Move to template - which CSS style?
#            context['markdown_text'] = self.request.user.get_full_name() + ': [ <a href="?edit=1">Edit Page</a> ]'
#        else:
#            context['markdown_text'] = ''

        try:
            context['markdown_text'] = get_md_cms_file_content(self, md_cms_file)
        except:
            # The file does not exist
            if self.request.user and self.request.user.is_superuser:
                context['md_cms_edit'] = True

                if self.request.GET and self.request.GET['edit']:
                    # Create the file
                    context['markdown_text'] = create_md_cms_file(md_cms_file)
#                else:
                    # Give option to create the file - move to template
#                    context['markdown_text'] = self.request.user.get_full_name() + ': No file found. [ <a href="?create=1">Create a Page</a> ]'
            else:
                raise Http404('Sorry, the requested page was not found.')

        return context
