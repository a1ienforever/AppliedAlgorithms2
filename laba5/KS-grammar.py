import ply.lex as lex

tokens = (
    'XMLDECL', 'OPEN_TAG', 'CLOSE_TAG', 'SELF_CLOSING_TAG',
    'COMMENT', 'TEXT', 'ENTITY'
)

t_XMLDECL = r'<\?xml[^?]*\?>'
t_OPEN_TAG = r'<[a-zA-Z_:][\w:.-]*(\s+[a-zA-Z_:][\w:.-]*="[^"]*")*\s*>'
t_CLOSE_TAG = r'</[a-zA-Z_:][\w:.-]*>'
t_SELF_CLOSING_TAG = r'<[a-zA-Z_:][\w:.-]*(\s+[a-zA-Z_:][\w:.-]*="[^"]*")*\s*/>'
t_COMMENT = r'<!--(.*?)-->'
t_TEXT = r'[^<>&]+'
t_ENTITY = r'&[a-zA-Z]+;'


t_ignore = ' \t\n'

def t_error(t):
    t.lexer.skip(1)
    raise "Illegal character '{t.value[0]}'"


lexer = lex.lex()

data = '''
<?xml version="1.0"?>
<root>
    <child attr="value">Hello, world!</child>
    <!-- Comment -->
    <self-closing/>
</root>
'''

if __name__ == '__main__':
    lexer.input(data)
    for tok in lexer:
        print(tok)
