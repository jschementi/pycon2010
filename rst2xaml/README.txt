A XAML writer from `reStructured Text <http://docutils.sourceforge.net>`_ source.

The goal is to be able to write out 
`FlowDocument XAML <http://msdn.microsoft.com/en-us/library/aa970909.aspx>`_ 
from ReST documents for use in WPF and Silverlight / 
`Moonlight <http://www.mono-project.com/Moonlight>`_ projects.

It includes a `Pygments <http://pygments.org>`_ formatter for outputting a
syntax highlighted XAML representation of source code.

rst2xaml itself runs under CPython, but the generated XAML is intended for use
from IronPython (or any other .NET language). There is an example IronPython
script for displaying the generated XAML using a WPF
`FlowDocumentReader <http://msdn.microsoft.com/en-us/library/system.windows.controls.flowdocumentreader.aspx>`_.


Requirements
------------

rst2xaml depends on:

* `docutils <http://docutils.sourceforge.net/>`_
* Pygments_

Tested with Python 2.5 and 2.6, but probably works fine under Python 2.4.

The Silverlight output is intended to work with Moonlight (the equivalent of Silverlight 2) *and* Silverlight 3. Let me know if
there are any problems.


Current status
--------------

The docutils writer for both FlowDocument and Silverlight XAML can currently handle the following
markup features:

 * title and headings
 * paragraphs
 * bold
 * italics
 * literal blocks
 * inline literals
 * line blocks
 * bullet lists
 * enumerated lists
 * blockquotes
 * the raw:: xaml directive
 * the pygments code-block directive

In addition the FlowDocument output can handle superscript, although that only works for fonts that support it.

Nested enumerated lists don't yet work correctly for either FlowDocument or Silverlight output.

Scripts
-------

There are three scripts that come with rst2xaml::

    python rst2xaml.py source.txt output.xaml
    python rst2xamlsl.py silverlight-source.txt silverlight-output.xaml
    ipy.exe display_xaml.py output.xaml

If ``display_xaml.py`` is run without a command line argument it will open a
file dialog for you to choose a xaml file to display.


Tests
-----

The tests use the `discover module <http://pypi.python.org/pypi/discover>`_,
which is included in the repository for convenience. You run the tests with:

    `python discover.py`
    

Development
-----------

The development version of rst2xaml is hosted on a google project page:

* http://code.google.com/p/rst2xaml/


CHANGELOG
---------

2009/09/XX Version X.X.X
~~~~~~~~~~~~~~~~~~~~~~~~

Pygments code blocks and literal blocks are indented to the right in the
Silverlight output.

BUGFIX: In the pygments formatter unknown tokens are now based on their parents,
as they always should have been...


2009/08/29 Version 0.1.1
~~~~~~~~~~~~~~~~~~~~~~~~

Bottom margin on list items increased.

Addition of xclass option for the Silverlight XAML, for use from
`Try Python <http://www.trypython.org>`_.


2009/08/20 Version 0.1.0
~~~~~~~~~~~~~~~~~~~~~~~~

Initial release.


