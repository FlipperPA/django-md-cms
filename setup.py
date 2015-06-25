import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-md-cms',
    version='0.1',
    packages=['md_cms'],
    include_package_data=True,
    license='BSD License',
    description='A simple Django CMS which reads markdown files from the filesystem based on the Django route and provides the Pagedown editor.',
    long_description=README,
    long_description=open('README.md', encoding='utf-8').read(),
    url='https://github.com/FlipperPA/django-md-cms',
    author='Timothy Allen',
    author_email='tim@pyphilly.org',
    install_required=[
        'django-pagedown==0.1.0',
        'Markdown==2.6.2',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
