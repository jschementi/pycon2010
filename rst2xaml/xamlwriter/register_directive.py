
from pygments import highlight
from pygments.lexers import get_lexer_by_name #, TextLexer

from docutils import nodes
from docutils.parsers.rst import directives

from xamlwriter.xamlformatter import XamlFormatter

# set externally to configure whether FlowDocument or Silverlight
# XAML is to be output
flowdocument = True

# set externally to configure if code blocks are stored
store_code_blocks = False
code_blocks = []

def process_lines(lines):
    output = []
    for line in lines:
        if line[:4] in ('... ', '>>> ', '...', '>>>'):
            output.append(line[4:])
    return output

def pygments_directive(name, arguments, options, content, lineno,
                       content_offset, block_text, state, state_machine):
    if store_code_blocks:
        if arguments[0] == 'python':
            code_blocks.append(list(content))
        elif arguments[0] == 'pycon':
            code_blocks.append(process_lines(list(content)))
    #print 'working on'
    #print '\n'.join(content)
    #try:
    lexer = get_lexer_by_name(arguments[0])
    #except ValueError:
        # no lexer found - use the text one instead of an exception
    #    lexer = TextLexer()
    # take an arbitrary option if more than one is given
    formatter = XamlFormatter(flowdocument=flowdocument, 
                              store_code_blocks=store_code_blocks)
    parsed = highlight(u'\n'.join(content), lexer, formatter)
    return [nodes.raw('', parsed, format='xaml')]

pygments_directive.arguments = (1, 0, 1)
pygments_directive.content = 1
pygments_directive.options = {}

directives.register_directive('code-block', pygments_directive)
