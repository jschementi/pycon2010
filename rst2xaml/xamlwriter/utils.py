
# Using XAML escape rules (XML) from:
# http://msdn.microsoft.com/en-us/library/ms748250.aspx

def escape_xaml(text):
    """Escape &, <, > as well as single and double quotes for XML."""
    return text.replace('&', '&amp;').  \
                replace('<', '&lt;').   \
                replace('>', '&gt;').   \
                replace('"', '&quot;'). \
                replace("'", '&apos;')
