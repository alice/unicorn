class Node(object):
    """Base class for all parse tree nodes"""
    def __init__(self, type):
        self.type = type;

class StmtList(Node):
    """A list of statements"""
    stmts = []
    def __init__(self):
        Node.__init__(self, 'stmt_list')

    def __str__(self):
        return ', '.join([str(stmt) for stmt in self.stmts])

    def add_stmt(self, stmt):
        """Append a statement to the list"""
        self.stmts.append(stmt)

    def execute(self):
        """Execute all statements in the list in order"""
        for stmt in self.stmts:
            print 'executing %s' % str(stmt)
            stmt.execute()

class Stmt(Node):
    """Base class for all statement types"""
    def __init__(self, type):
        Node.__init__(self, type)

    def execute(self):
        """Execute this statement. To be implemented by each subclass."""
        raise Exception('execute not implemented for base Stmt class')

class AssignStmt(Stmt):
    """Assignment statement"""
    # Example: x <- 3
    name = None  # 'x' in example
    rhs = None   # '3' in example

    def __init__(self, name):
        Node.__init__(self, 'assignment')
        self.name = name

    def __str__(self):
        return '%s <- %s' % (self.name, str(self.rhs))

    def execute(self):
        global context
        context[self.name] = self.rhs.value()
        print 'set %s <- %s', (self.name, self.rhs.value())

class PrintStmt(Stmt):
    """Print statement"""
    atoms_to_print = []

    def __init__(self):
        Node.__init__(self, 'print_stmt')

    def __str__(self):
        return 'show %s' % ' '.join([str(a) for a in self.atoms_to_print])

    def add_atom(self, atom):
        """Append the atom to the list of atoms to be printed"""
        self.atoms_to_print.append(atom)

    def execute(self):
        print ''.join([str(a.value()) for a in self.atoms_to_print])

class Atom(Node):
    """Base class for all atom types"""
    def __init__(self, type, val):
        Node.__init__(self, type)
        self.val = val

    def value(self):
        """Get the value of this atom"""
        return self.val

class Name(Atom):
    """Atom class for name (identifier)"""
    def __init__(self, name):
        Atom.__init__(self, 'NAME', name)

    def __str__(self):
        return self.val

    def value(self):
        """Looks up the value of this name in the global context"""
        global context
        if self.val not in context:
            raise Exception('Name %s not found in context' % self.val)
        return context[self.val]

class String(Atom):
    """Atom class for string"""
    def __init__(self, str_val):
        Atom.__init__(self, 'STRING', str_val)

    def __str__(self):
        return '"%s"' % self.val

class Number(Atom):
    """Atom class for number"""
    def __init__(self, int_val):
        Atom.__init__(self, 'NUMBER', int_val)

    def __str__(self):
        return str(self.val)

def getsym():
    """Get the next token"""
    global tokens
    global sym
    if len(tokens) > 0:
        sym = tokens.pop(0)
    else:
        sym = None

def accept(s):
    """'Eat' a token of type s"""
    global sym
    type, _ = sym
    if (type == s):
        getsym()
        return True
    return False;

def expect(s):
    """
      'Eat' a token of type 's', throw an exception if the next token is not
      the right type
    """
    global sym
    if accept(s):
        return True
    raise Exception("Unexpected symbol %s" % str(sym))

def parse_stmt_list():
    stmt_list = StmtList()
    stmt, success = parse_stmt()
    while success:
        stmt_list.add_stmt(stmt)
        stmt, success = parse_stmt()
    return stmt_list
    # TODO handle extra tokens

def parse_stmt():
    global sym
    if sym == None:
        return (None, False)
    stmt, success = parse_simple_stmt()
    if not success:
        stmt, success = parse_compound_stmt()
    if not success:
        return (None, False)
    expect('newline')
    return (stmt, True)


def parse_simple_stmt():
    stmt, success = parse_print_stmt()
    if not success:
        stmt, success = parse_assignment()
    if not success:
        return (None, False)
    return (stmt, True)

def parse_compound_stmt():
    # Not yet implemented
    return False

def parse_assignment():
    global sym
    type, name = sym
    if type != 'id':
        print 'Expected id'
        return (None, False)
    getsym()
    expect('op_assign')

    # TODO parse_expr
    atom, success = parse_atom()
    if not success:
        raise Exception('Expected value in assignment')
    getsym()

    assign_stmt = AssignStmt(name)
    assign_stmt.rhs = atom
    return (assign_stmt, True)

def parse_print_stmt():
    global sym
    if not accept('show'):
        return (None, False)
    print_stmt = PrintStmt()
    atom, success = parse_atom()
    if not success:
        raise Exception('Expected at least one value to show')
    while success:
        print_stmt.add_atom(atom)
        getsym()
        atom, success = parse_atom()
    return (print_stmt, True)

def parse_atom():
    global sym
    type, value = sym
    if type == 'id':
        name = Name(value)
        return (name, True)
    elif type == 'int':
        number = Number(value)
        return (number, True)
    elif type == 'string':
        string = String(value)
        return (string, True)

    return (None, False)

def parse(toks):
    global tokens
    tokens = toks
    global context
    context = {}
    getsym()
    stmt_list = parse_stmt_list()
    print str(stmt_list)
    stmt_list.execute()
