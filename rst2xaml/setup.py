from distutils.core import setup
from xamlwriter import __version__ as version

description = """A docutils writer for FlowDocument XAML.

Includes an ``rst2xaml`` script that takes a reStructured Text source document
and outputs a XAML document.

FlowDocument XAML is a text markup for displaying documents in the Microsoft
Windows Presentation Foundation (WPF) user interface - which is also used in
the Silverlight / Moonlight browser plugins.

The goal is to be able to write Python tutorials in reST and present them on the
web with a Python interactive interpreter running in the browser. This will also
require XAML output from Pygments."""


setup(
    name='rst2xaml',
    version=version,
    description=description,
    author="Michael Foord",
    author_email="michael@voidspace.org.uk",
    packages= ['xamlwriter', 'xamlwriter.tests', 'xamlwriter.modules'],
    scripts=['rst2xaml.py', 'rst2xamlsl.py', 'display_xaml.py']
)
