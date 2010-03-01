import unittest
from textwrap import dedent
from docutils.core import publish_string

from xamlwriter.node import Node, TextNode
from xamlwriter.translator import FONT_SIZE, MARGIN, FONTS, MONOSPACE
from xamlwriter.writer import XamlWriter, publish_xaml


settings_overrides = {
    'file_insertion_enabled': False,
}

def tree_from_string(input_data):
    input_data = dedent(input_data)
    rv = publish_string(source=input_data, writer=XamlWriter(),
                        settings_overrides=settings_overrides)

    return rv.root


def get_root():
    node = Node('FlowDocument')
    node.attributes['FontSize'] = FONT_SIZE
    node.attributes['xmlns'] = "http://schemas.microsoft.com/winfx/2006/xaml/presentation"
    node.attributes['xmlns:x'] = "http://schemas.microsoft.com/winfx/2006/xaml"
    return node


def tree_from_string_sl(input_data):
    input_data = dedent(input_data)
    writer = XamlWriter(flowdocument=False)
    rv = publish_string(source=input_data, writer=writer,
                        settings_overrides=settings_overrides)

    return rv.root


def get_root_sl():
    node = Node('StackPanel')
    node.attributes['x:Class'] = 'System.Windows.Controls.StackPanel'
    node.attributes['xmlns'] = "http://schemas.microsoft.com/winfx/2006/xaml/presentation"
    node.attributes['xmlns:x'] = "http://schemas.microsoft.com/winfx/2006/xaml"
    return node


def get_sl_paragraph():
    para = Node('TextBlock')
    para.attributes['FontSize'] = FONT_SIZE
    para.attributes['Margin'] = "0,10,0,0"
    para.attributes['TextWrapping'] = "Wrap"
    para.attributes['FontFamily'] = FONTS
    return para

def get_grid_sl(items, enumerated=True):
    node = get_root_sl()
    grid = Node('Grid')
    grid.attributes['Margin'] = '0,10,0,0'
    node.children.append(grid)
    columns = Node('Grid.ColumnDefinitions')
    grid.children.append(columns)
    col = Node('ColumnDefinition')
    col.attributes['Width'] = 'Auto'
    columns.children.append(col)
    columns.children.append(Node('ColumnDefinition'))
    rows = Node('Grid.RowDefinitions')
    grid.children.append(rows)
    rows.children = [Node('RowDefinition') for _ in items]
    
    for i, item in enumerate(items):
        bullet = Node('TextBlock')
        point = '&#8226;'
        if enumerated:
            point = str(i + 1) + '.'
        bullet.attributes['Grid.Row'] = str(i)
        bullet.attributes['Grid.Column'] = '0'
        bullet.attributes['FontFamily'] = FONTS
        bullet.children.append(TextNode(point))
                               
        bullet_text = Node('StackPanel')
        bullet_text.attributes['Margin'] = "5,0,0,5"
        bullet_text.attributes['Grid.Row'] = str(i)
        bullet_text.attributes['Grid.Column'] = '1'
        para = get_sl_paragraph()
        del para.attributes['Margin']
        para.children.append(TextNode(item))
        bullet_text.children.append(para)
        
        grid.children.append(bullet)
        grid.children.append(bullet_text)
    return node



class TestXamlWriter(unittest.TestCase):

    def testBasic(self):
        tree = tree_from_string('')
        self.assertEqual(tree, get_root())
    
        
    def testParagraph(self):
        tree = tree_from_string('Hello')
        
        node = get_root()
        node.children.append(Node('Paragraph'))
        node.children[0].children.append(TextNode('Hello'))
        self.assertEqual(tree, node)

        
    def testXamlEscape(self):
        tree = tree_from_string('"&<\'>"')
        
        node = get_root()
        node.children.append(Node('Paragraph'))
        node.children[0].children.append(TextNode('&quot;&amp;&lt;&apos;&gt;&quot;'))
        self.assertEqual(tree, node)
    
        
    def testItalics(self):
        tree = tree_from_string('*Hello*')
        
        node = get_root()
        para = Node('Paragraph')
        para.children.append(Node('Italic'))
        para.children[0].children.append(TextNode('Hello'))
        node.children.append(para)
        self.assertEqual(tree, node)
    
        
    def testBold(self):
        tree = tree_from_string('**Hello**')
        
        node = get_root()
        para = Node('Paragraph')
        para.children.append(Node('Bold'))
        para.children[0].children.append(TextNode('Hello'))
        node.children.append(para)
        self.assertEqual(tree, node)
    
        
    def testBlockquote(self):
        tree = tree_from_string('Hello\n\n    foo\n')
        
        node = get_root()
        para = Node('Paragraph')
        para.children.append(TextNode('Hello'))
        node.children.append(para)
        
        section = Node('Section')
        section.attributes['Margin'] = "16,0,0,0"
        quote = Node('Paragraph')
        quote.children.append(TextNode('foo'))
        section.children.append(quote)
        
        node.children.append(section)
        
        self.assertEqual(tree, node)


    def testRawXaml(self):
        data = '.. raw:: xaml\n\n   foo'
        output = publish_xaml(data)
        node = get_root()
        node.children.append(TextNode('foo'))
        self.assertEqual(output, node.to_string())
        
    
    def testLiteralBlock(self):
        node = get_root()
        literal = Node('Paragraph')
        literal.attributes['FontFamily'] = MONOSPACE
        literal.attributes['xml:space'] = 'preserve'
        node.children.append(literal)
        literal.children.append(TextNode('foo'))
        
        self.assertEqual(tree_from_string('::\n\n    foo'), node)
    
       
    def testSuperscript(self):
        node = get_root()
        para = Node('Paragraph')
        superscript = Node('Run')
        superscript.attributes['Typography.Variants'] = 'Superscript'
        para.children.append(superscript)
        node.children.append(para)
        superscript.children.append(TextNode('foo'))
        
        self.assertEqual(tree_from_string(':sup:`foo`'), node)
    
    
    def testLineBlock(self):
        node = get_root()
        para = Node('Paragraph')
        para.children.append(TextNode('foo'))
        para.children.append(Node('LineBreak'))
        para.children.append(TextNode('bar'))
        para.children.append(Node('LineBreak'))
        
        node.children.append(para)
        
        actual = tree_from_string("""\
            | foo
            | bar""")
        
        self.assertEqual(actual, node)
    
    
    def testBulletList(self):
        node = get_root()
        def get_item(text):
            node = Node('ListItem')
            para = Node('Paragraph')
            para.children.append(TextNode(text))
            node.children.append(para)
            return node
        
        list_node = Node('List')
        list_node.children.append(get_item('first'))
        list_node.children.append(get_item('second'))
        list_node.children.append(get_item('third'))
        
        node.children.append(list_node)
        
        actual = tree_from_string("""\
            * first
            * second
            * third""")
        
        self.assertEqual(actual, node)
    
    
    def testEnumeratedList(self):
        node = get_root()
        def get_item(text):
            node = Node('ListItem')
            para = Node('Paragraph')
            para.children.append(TextNode(text))
            node.children.append(para)
            return node
        
        list_node = Node('List')
        list_node.attributes['MarkerStyle'] = 'Decimal'
        list_node.children.append(get_item('first'))
        list_node.children.append(get_item('second'))
        list_node.children.append(get_item('third'))
        
        node.children.append(list_node)
        
        actual = tree_from_string("""\
            1. first
            2. second
            3. third""")
        
        self.assertEqual(actual, node)
        
    
    def testLiteral(self):
        node = get_root()
        para = Node('Paragraph')
        literal = Node('Run')
        literal.attributes['FontFamily'] = MONOSPACE
        literal.attributes['xml:space'] = 'preserve'
        para.children.append(literal)
        literal.children.append(TextNode('foo  bar'))
        node.children.append(para)
        
        self.assertEqual(tree_from_string('``foo  bar``'), node)

    def testTitleSubtitleSection(self):
        def get_title(fontsize, text, **attributes):
            node = Node('Paragraph')
            node.children.append(TextNode(text))
            node.attributes.update(attributes.items())
            node.attributes['FontSize'] = str(fontsize)
            return node
        
        node = get_root()
        node.children.append(get_title(20, 'Title', FontWeight='Bold'))
        node.children.append(get_title(19, 'Subtitle', FontStyle='Italic'))
        node.children.append(get_title(19, 'Heading 1'))
        node.children.append(get_title(18, 'Heading 2'))
        node.children.append(get_title(17, 'Heading 3'))
        node.children.append(get_title(16, 'Heading 4'))
        
        source = """\
        =======
         Title
        =======
        ----------
         Subtitle
        ----------
        
        Heading 1
        =========
        
        Heading 2
        ---------
        
        Heading 3
        ~~~~~~~~~
        
        Heading 4
        #########
        """
        result = tree_from_string(source)
        self.assertEqual(result, node)



class TestSilverlightXaml(unittest.TestCase):

    def testBasic(self):
        tree = tree_from_string_sl('')
        self.assertEqual(tree, get_root_sl())

        
    def testParagraph(self):
        tree = tree_from_string_sl('Hello')
        
        node = get_root_sl()
        para = get_sl_paragraph()
        node.children.append(para)
        node.children[0].children.append(TextNode('Hello'))
        self.assertEqual(tree, node)
    
        
    def testItalics(self):
        tree = tree_from_string_sl('*Hello*')
        
        node = get_root_sl()
        para = get_sl_paragraph()
        italic = Node('Run')
        italic.attributes['FontStyle'] = 'Italic'
        para.children.append(italic)
        para.children[0].children.append(TextNode('Hello'))
        
        node.children.append(para)
        self.assertEqual(tree, node)
    
        
    def testBold(self):
        tree = tree_from_string_sl('**Hello**')
        
        node = get_root_sl()
        para = get_sl_paragraph()
        italic = Node('Run')
        italic.attributes['FontWeight'] = 'Bold'
        para.children.append(italic)
        para.children[0].children.append(TextNode('Hello'))
        
        node.children.append(para)
        self.assertEqual(tree, node)


    def testBlockquote(self):
        tree = tree_from_string_sl('Hello\n\n    foo\n')
        
        node = get_root_sl()
        para = get_sl_paragraph()
        para.children.append(TextNode('Hello'))
        node.children.append(para)
        
        block = Node('StackPanel')
        block.attributes['Margin'] = MARGIN
        para2 = get_sl_paragraph()
        para2.children.append(TextNode('foo'))
        block.children.append(para2)
        
        node.children.append(block)
        
        self.assertEqual(tree, node)
        

    def testRawXaml(self):
        data = '.. raw:: xaml\n\n   foo'
        output = publish_xaml(data, flowdocument=False)

        node = get_root_sl()
        node.children.append(TextNode('foo'))
        self.assertEqual(output, node.to_string())
        
    
    def testLiteralBlock(self):
        node = get_root_sl()
        
        literal = get_sl_paragraph()
        literal.attributes['Margin'] = "15,10,0,0"
        literal.attributes['FontFamily'] = MONOSPACE
        # XXXX do we want the literal paragraph (TextBlock) to have NoWrap set?
        node.children.append(literal)
        
        literal.children.append(TextNode('foo'))
        literal.children.append(Node('LineBreak'))
        literal.children.append(TextNode('foo&#160;&#160;foo'))
        
        result = tree_from_string_sl('::\n\n    foo\n    foo  foo\n')
        self.assertEqual(result, node)
    
    
    def testLineBlock(self):
        node = get_root_sl()
        para = get_sl_paragraph()
        para.children.append(TextNode('foo'))
        para.children.append(Node('LineBreak'))
        para.children.append(TextNode('bar'))
        
        node.children.append(para)
        
        actual = tree_from_string_sl("""\
            | foo
            | bar""")
        
        self.assertEqual(actual, node)
    
    
    def testBulletList(self):
        node = get_grid_sl(['first', 'second', 'third'], enumerated=False)
        actual = tree_from_string_sl("""\
            * first
            * second
            * third""")
        
        self.assertEqual(actual, node)
    
    
    def testEnmeratedList(self):
        node = get_grid_sl(['first', 'second', 'third'])
        actual = tree_from_string_sl("""\
            #. first
            #. second
            #. third""")
        
        self.assertEqual(actual, node)
        
    
    def testLiteral(self):
        node = get_root_sl()
        para = get_sl_paragraph()
        literal = Node('Run')
        literal.attributes['FontFamily'] = MONOSPACE
        para.children.append(literal)
        literal.children.append(TextNode('foo&#160;&#160;bar'))
        node.children.append(para)
        
        self.assertEqual(tree_from_string_sl('``foo  bar``'), node)
        
        
    def testTitleSubtitleSection(self):
        def get_title(fontsize, text, FontWeight=None, FontStyle=None):
            node = Node('TextBlock')
            node.children.append(TextNode(text))
            if FontWeight is not None:
                node.attributes['FontWeight'] = FontWeight
            node.attributes['Margin'] = "0,10,0,0"
            node.attributes['FontFamily'] = FONTS
            if FontStyle is not None:
                node.attributes['FontStyle'] = FontStyle
            node.attributes['FontSize'] = str(fontsize)
            return node
        
        node = get_root_sl()
        node.children.append(get_title(20, 'Title', FontWeight='Bold'))
        node.children.append(get_title(19, 'Subtitle', FontStyle='Italic'))
        node.children.append(get_title(19, 'Heading 1'))
        node.children.append(get_title(18, 'Heading 2'))
        node.children.append(get_title(17, 'Heading 3'))
        node.children.append(get_title(16, 'Heading 4'))
        
        source = """\
        =======
         Title
        =======
        ----------
         Subtitle
        ----------
        
        Heading 1
        =========
        
        Heading 2
        ---------
        
        Heading 3
        ~~~~~~~~~
        
        Heading 4
        #########
        """
        result = tree_from_string_sl(source)
        self.assertEqual(result, node)




if __name__ == '__main__':
    unittest.main()
