import unittest

from textwrap import dedent

from xamlwriter.writer import publish_xaml

# This installs the pygments directive
import xamlwriter.register_directive


def make_source(string):
    return ('.. code-block:: python\n\n    ' +
            '\n    '.join(string.splitlines()))

def make_doc(string):
    return ('<FlowDocument FontSize="15" xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation" '
            'xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml">'
            '<Paragraph FontFamily="Consolas, Monaco, Lucida Console, Global Monospace" xml:space="preserve">%s'
            '</Paragraph></FlowDocument>' % string)

def make_doc_sl(string):
    return ('<StackPanel x:Class="System.Windows.Controls.StackPanel" '
            'xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation" '
            'xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml">'
            '<TextBlock FontFamily="Consolas, Monaco, Lucida Console, Global Monospace" FontSize="15" Margin="15,10,0,0">'
            '%s</TextBlock></StackPanel>') % string

def make_doc_with_store_code_block(string):
    return ('<StackPanel x:Class="System.Windows.Controls.StackPanel" '
            'xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation" '
            'xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml">'
            '<TextBlock FontFamily="Consolas, Monaco, Lucida Console, Global Monospace" FontSize="15" Margin="15,10,0,0">'
            '%s</TextBlock></StackPanel>') % string
    

class TestPygments(unittest.TestCase):
    
    def testComment(self):
        # smoke test
        source = make_source('# comment')
        
        expected = make_doc('<Run Foreground="#408080" FontStyle="Italic"># comment</Run><Run></Run>\n')
        self.assertEqual(publish_xaml(source), expected)
    

    def testXamlEscape(self):
        source = make_source('"&<\'>"')
        expected = make_doc('<Run Foreground="#BA2121">&quot;&amp;&lt;&apos;&gt;&quot;</Run><Run></Run>\n')
        self.assertEqual(publish_xaml(source), expected)

        
    def testSilverlightWhitespaceHandling(self):
        xamlwriter.register_directive.flowdocument = False
        try:
            source = make_source('"foo  foo"\n"foo  foo"')
            expected = make_doc_sl('<Run Foreground="#BA2121">'
                                '&quot;foo&#0160;&#0160;foo&quot;</Run>'
                                '<Run></Run><LineBreak />'
                                '<Run Foreground="#BA2121">'
                                '&quot;foo&#0160;&#0160;foo&quot;</Run>'
                                '<Run></Run><LineBreak />')
            self.assertEqual(publish_xaml(source, flowdocument=False), expected)
        finally:
            xamlwriter.register_directive.flowdocument = True


    def testStoreCodeBlocks(self):
        try:
            from xamlwriter import register_directive
            register_directive.store_code_blocks = True
            register_directive.code_blocks = []
            self.fail()
        finally:
            register_directive.store_code_blocks = False
            register_directive.code_blocks = []
            




if __name__ == '__main__':
    unittest.main()
