# Django Markdown CMS (md_cms)
Django Markdown CMS: A markdown flat-file based CMS for Django.

## Objectives:
* To create a flat-file based CMS so content is portable, and easily stored in version control
* All source content will be in markdown, making it portable / exportable to other formats
* Plug-and-Play tie-in to Django's cache framework
* Inherit slug from urls.py to edit or create a new file.
* Ability to include a markdown file as a fragment within a Django template:
    * `{% md-cms "about/welcome.md" %}`

## Dependencies:
* django
* python-markdown
* django-pagedown https://github.com/timmyomahony/django-pagedown
* bleach

## Installation:
* Install via pip:
    * `pip install django-md-cms`
* Add to INSTALLED_APPS in your settings:
    * `INSTALLED_APPS += ('md_cms',)`

## Settings:
* MD_CMS_ROOT: the root location of files accessible within the CMS. Please note, this path does **not** have to be web accessible.
* MD_CMS_DEFAULT_FILE: if a path is provided with no file, the default file name to use.
* MD_CMS_EDIT_SUFFIX: suffix to append to the urlpattern from urls.py to trigger the Pagedown editor.
* Example:

`
    DJANGO_MD_CMS_ROOT = '/var/md_cms_content'
    MD_CMS_DEFAULT_FILE = 'index.md'
    MD_CMS_EDIT_SUFFIX = 'edit'
`

## Example 1:

This example shows how to have django-md-cms control all the content for your site.

    django-admin.py startproject myproject
    pip install django-md-cms
    cd myproject && python manage.py migrate
    python manage.py createsuperuser

Then, edit your `uls.py` file, to look something like this:

    from django.conf.urls import include, url
    from django.contrib import admin
    from md_cms.views import MdCMSView

    urlpatterns = [
        url(r'^admin/', include(admin.site.urls)),
        url(r'^([A-Za-z0-9-/]*)/$', MdCMSView.as_view(), name='pages'),
    ]

This set of patterns first looks for the Django Admin, then for any HTTP_INFO pattern matching any letter (upper or lowercase), a hyphen ('-'), or a foreward slash ('/'). These will result in the creation of valid system paths and files.


## A Note About URLs: /this-page != /this_page/

Trailing slashes matter in your URLs! The way the logic is constructed is as follows:

* /this-page will create a file named `DJANGO_MD_CMS_ROOT + '/this-page.md'`
* /this-page/ will create a directory named `DJANGO_MD_CMS_ROOT + '/this-page/'` and a file named `DJANGO_MD_CMS_ROOT + '/this-page/index.md'`

