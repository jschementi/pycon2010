import copy
import re

from docutils import nodes
from docutils.nodes import NodeVisitor, SkipNode

from xamlwriter.node import ErrorNode, Node, TextNode
from xamlwriter.utils import escape_xaml


FONT_SIZE = '15'
MARGIN = "16,0,0,0" 
FONTS = 'Verdana,Tahoma,Geneva,Lucida Grande,Trebuchet MS,Helvetica,Arial,Serif'
MONOSPACE = "Consolas, Monaco, Lucida Console, Global Monospace"

class XamlTranslator(NodeVisitor):

    def __init__(self, document, flowdocument=True, xclass=True):
        NodeVisitor.__init__(self, document)
        self.flowdocument = flowdocument
        if flowdocument:
            self.root = Node('FlowDocument')
            self.root.attributes['FontSize'] = FONT_SIZE
        else:
            self.root = Node('StackPanel')
            if xclass:
                self.root.attributes['x:Class'] = 'System.Windows.Controls.StackPanel'
        self.root.attributes['xmlns'] = "http://schemas.microsoft.com/winfx/2006/xaml/presentation"
        self.root.attributes['xmlns:x'] = "http://schemas.microsoft.com/winfx/2006/xaml"
        self.curnode = self.root
        self.context = []
        self.initial_header_level = 2
        self.section_level = 0
        self.in_literal = False
        self.list_item = 0
        self.done_first_item = True
        self.bullet_list = True

    def begin_node(self, node, tagname, **more_attributes):
        new_node = Node(tagname)
        attributes = new_node.attributes
        for name, value in more_attributes.iteritems():
            attributes[name] = value
        if node is not None:
            # ids and classes handled here
            pass
        new_node.parent = self.curnode
        self.curnode.children.append(new_node)
        self.curnode = new_node

    def end_node(self):
        self.curnode = self.curnode.parent

    def add_text(self, text, escape=True):
        if not text:
            return
        if escape:
            text = escape_xaml(text)
        if not self.in_literal:
            self.curnode.children.append(TextNode(text))
            return
        assert not self.flowdocument
        text = text.replace(' ', '&#160;')
        parts = text.split('\n')
        for part in parts[:-1]:
            self.curnode.children.append(TextNode(part))
            self.curnode.children.append(Node('LineBreak'))
        self.curnode.children.append(TextNode(parts[-1]))

    def add_node(self, name, text='', escape=True, **attributes):
        self.begin_node(None, name, **attributes)
        self.add_text(text, escape=escape)
        self.end_node()

    def unknown_visit(self, node):
        # should raise here or indicate unsupported feature some way
        return

    def unknown_departure(self, node):
        return

    trivial_nodes_flowdocument = {
        'paragraph': ('Paragraph', {}),
        'emphasis': ('Italic', {}),
        'strong': ('Bold', {}),
        'block_quote': ('Section', {'Margin': MARGIN}),
        'literal_block': ('Paragraph', {'FontFamily': 'Consolas, Monaco, Lucida Console, Global Monospace', 
                                        'xml:space': 'preserve'}),
        'superscript': ('Run', {'Typography.Variants': 'Superscript'}),
        'line_block': ('Paragraph', {}), 
        'bullet_list': ('List', {}),
        'list_item': ('ListItem', {}),
        'enumerated_list': ('List', {'MarkerStyle': 'Decimal'}),
        'literal': ('Run', {'FontFamily': 'Consolas, Monaco, Lucida Console, Global Monospace', 
                            'xml:space': 'preserve'})
    }
    
    trivial_nodes_silverlight = {
        'emphasis': ('Run', {'FontStyle': 'Italic'}),
        'strong': ('Run', {'FontWeight': 'Bold'}),
        'block_quote': ('StackPanel', {'Margin': MARGIN}),
    }
    
    @property
    def trivial_nodes(self):
        if self.flowdocument:
            return self.trivial_nodes_flowdocument
        return self.trivial_nodes_silverlight
        

    def dispatch_visit(self, node):
        # don't call visitor methods for trivial nodes
        node_name = node.__class__.__name__
        if node_name == 'Text':
            self.add_text(node.astext())
            raise SkipNode
            
        tagname, atts = self.trivial_nodes.get(node_name, (None, None))
        if tagname:
            self.begin_node(node, tagname, **atts)
        else:
            getattr(self, 'visit_' + node_name, self.unknown_visit)(node)

    def dispatch_departure(self, node):
        node_name = node.__class__.__name__
        
        tagname, atts = self.trivial_nodes.get(node_name, (None, None))
        if tagname:
            self.end_node()
        else:
            getattr(self, 'depart_' + node_name, self.unknown_departure)(node)

    def visit_raw(self, node):
        if 'xaml' in node.get('format', '').split():
            self.curnode.children.append(TextNode(node.astext()))
        raise SkipNode
    
    def visit_paragraph(self, node):
        # Silverlight only
        attrs = {'FontSize': FONT_SIZE, 'TextWrapping': "Wrap", 'FontFamily': FONTS}
        if self.done_first_item:
            attrs['Margin'] = "0,10,0,0"
        self.begin_node(node, 'TextBlock', **attrs)
        self.done_first_item = True
        
    def depart_paragraph(self, node):
        self.end_node()
    
    def visit_line_block(self, node):
        # Silverlight only
        self.begin_node(node, 'TextBlock', Margin= "0,10,0,0", FontSize=FONT_SIZE, TextWrapping="Wrap", FontFamily=FONTS)
        
    def depart_line_block(self, node):
        if self.curnode.children[-1] == Node('LineBreak'):
            self.curnode.children.pop()

        self.end_node()
        
    def visit_line(self, node):
        pass
    
    def depart_line(self, node):
        self.add_node('LineBreak')
    
    def visit_title(self, node):
        begun = False
        node_type = 'Paragraph'
        attrs = {}
        if not self.flowdocument:
            node_type = 'TextBlock'
            attrs['Margin'] = '0,10,0,0'
            attrs['FontFamily'] = FONTS
        if isinstance(node.parent, nodes.document):
            begun = True
            self.begin_node(node, node_type, FontSize='20', FontWeight='Bold', **attrs)
        elif isinstance(node.parent, nodes.section):
            if (len(node.parent) >= 2 and
                isinstance(node.parent[1], nodes.subtitle)):
                attrs['FontStyle'] = 'Italic'
            attrs['FontSize'] = str(20 - self.section_level)
            self.begin_node(node, node_type, **attrs)
            begun = True
            # We don't do back-reference link for title
        else:
            # also used for sidebar, topic, 
            # Admonition, table (caption)
            pass
        self.context.append(begun)

    def depart_title(self, node):
        if self.context.pop():
            self.end_node()
    
    def visit_section(self, node):
        self.section_level += 1

    def depart_section(self, node):
        self.section_level -= 1
        
    def visit_subtitle(self, node):
        begun = False
        if isinstance(node.parent, nodes.document):
            node_type = 'Paragraph'
            attrs = {}
            if not self.flowdocument:
                node_type = 'TextBlock'
                attrs['Margin'] = '0,10,0,0'
                attrs['FontFamily'] = FONTS
            self.begin_node(node, node_type, FontSize='19',
                            FontStyle='Italic', **attrs)
            begun = True
        else:
            # Also used for sidebar and section
            pass
        self.context.append(begun)

    def depart_subtitle(self, node):
        if self.context.pop():
            self.end_node()
    
    def visit_literal_block(self, node):
        # only used for Silverlight
        self.in_literal = True
        self.begin_node(node, 'TextBlock', Margin="15,10,0,0", FontSize="15",
                        TextWrapping="Wrap", FontFamily=MONOSPACE)
        
    def depart_literal_block(self, node):
        self.in_literal = False
        self.end_node()
    
    def visit_enumerated_list(self, node):
        # only used for Silverlight
        self.bullet_list = False
        self.visit_bullet_list(node)
        
    def depart_enumerated_list(self, node):
        self.depart_bullet_list(node)
        
    def visit_bullet_list(self, node):
        # only used for Silverlight
        self.list_item = 0
        self.begin_node(node, 'Grid', Margin='0,10,0,0')
        self.begin_node(node, 'Grid.ColumnDefinitions')
        self.add_node('ColumnDefinition', Width='Auto')
        self.add_node('ColumnDefinition')
        self.end_node()

    def depart_bullet_list(self, node): 
        rows = Node('Grid.RowDefinitions')
        rows.children = [Node('RowDefinition') for _ in range(self.list_item)]
        self.curnode.children.insert(1, rows)
        self.end_node()
        self.bullet_list = True
        
    def visit_list_item(self, node):
        # only used for Silverlight
        self.done_first_item = False
        point = '&#8226;'
        if not self.bullet_list:
            point = str(self.list_item + 1) + '.'
        self.add_node('TextBlock', point, escape=False, 
                      **{'Grid.Column': '0', 'Grid.Row': str(self.list_item), 'FontFamily': FONTS})
        self.begin_node(node, 'StackPanel', Margin="5,0,0,5",
                      **{'Grid.Column': '1', 'Grid.Row': str(self.list_item)})
        self.list_item += 1

    def depart_list_item(self, node):
        self.done_first_item = True
        self.end_node()
    
    def visit_literal(self, node):
        # only used for Silverlight
        self.in_literal = True
        self.begin_node(node, 'Run', FontFamily='Consolas, Monaco, Lucida Console, Global Monospace')
    
    def depart_literal(self, node):
        self.in_literal = False
        self.end_node()



"""
Can use Floater for sidebar (FlowDocument).
"""