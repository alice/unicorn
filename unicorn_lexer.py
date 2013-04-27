import sys
import re

token_exprs = [
    (r'([ \t]+)',                None),
    (r'(^[ \t]*\n)',              None),
    (r'(\n)',                    'newline'),
    (r'([0-9]+)',                'int'),
    (r'"(.*)"',                  'string'),
    (r"'(.*)'",                  'string'),
    (r'(<-)',                    'op_assign'),
    (r'(\?)',                    '?'),
    (r'(\()',                    'open_paren'),
    (r'(\))',                    'close_paren'),
    (r'(:)',                     'colon'),
    (r'(\+)',                    '+'),
    (r'(-)',                     '-'),
    (r'(\*)',                    '*'),
    (r'(/)',                     '/'),
    (r'(<)',                     '<'),
    (r'(<=)',                    'le'),
    (r'(>)',                     '>'),
    (r'(>=)',                    'ge'),
    (r'(=)',                     'eq'),
    (r'(!=)',                    'ne'),
    (r'(=/=)',                   'ne'),
    (r'(and)',                   'and'),
    (r'(or)',                    'or'),
    (r'(not)',                   'not'),
    (r'(is)',                    'is'),
    (r'(then)',                  'then'),
    (r'(loop)',                  'loop'),
    (r'(starting)',              'starting'),
    (r'(otherwise)',             'otherwise'),
    (r'(show)',                  'show'),
    (r'(stop)',                  'stop'),
    (r'(end)',                   'end'),
    (r'(to)',                    'to'),
    (r'(using)',                 'using'),
    (r'(randomize)',             'randomize'),
    (r'(prompt)',                'prompt'),
    (r'([A-Za-z][A-Za-z0-9_]*)', 'id'),
    (r'\'',                      None),
]

value_tokens = set(['int',
                    'string',
                    'id'])

def lex(characters):
  pos = 0
  tokens = []
  while pos < len(characters):
    match = None
    for token_expr in token_exprs:
      pattern, token_type = token_expr
      regex = re.compile(pattern)
      match = regex.match(characters, pos)
      if match:
        text = match.group(1)
        if token_type:
          if (token_type in value_tokens):
            token = (token_type, text)
          else:
            token = (token_type, None)
#         token = token_type(text)
          tokens.append(token)
        break
    if not match:
      sys.stderr.write('Illegal character: %s\n' % characters[pos])
      sys.exit(1)
    else:
      pos = match.end(0)
  return tokens
