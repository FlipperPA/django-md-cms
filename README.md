# Django Markdown CMS (md_cms)
Django Markdown CMS: A markdown flat-file based CMS for Django.

## Objectives:
* To create a flat-file based CMS so content is portable, and easily stored in version control
* All source content will be in markdown, making it portable / exportable to other formats
* Plug-and-Play tie-in to Django's cache framework
* Inherit slug from urls.py to edit or create a new file.
* Ability to include a markdown file as a fragment within a Django template:
    * `{% md-cms "about/welcome.md" %}`

## Installation:
* Install via pip:
    * `pip install django-md-cms`
* Add to INSTALLED_APPS in your settings:
    * `INSTALLED_APPS += ('md_cms',)`

## Settings:
* MD_CMS_ROOT: the root location of files accessible within the CMS. Examples:
    * `DJANGO_MD_CMS_ROOT = MEDIA_ROOT + 'md-cms/'`
    * `DJANGO_MD_CMS_ROOT = '/var/md-cms-files/'`

