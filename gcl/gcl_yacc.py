
import ply.yacc as yacc
from gcl_lex import tokens

precedence = (
		('nonassoc', 'IF', 'FI', 'DO', 'OD'),
		('nonassoc', 'SEMICOLON'),
		('nonassoc', 'ARROW'),
		('nonassoc', 'COMMA'),
		('nonassoc', 'ASSIGN'),
		('left', 'PLUS', 'MINUS'),
		('left', 'TIMES', 'DIVIDE'),
)

# parser rule은 top-down으로 제작

# 4. statement

def p_statement_one(p):
    '''statement : SKIP
                | ABORT
                | expression'''
    p[0] = p[1]


def p_statement_assign(p):
    'statement : variables ASSIGN expressions'
    p[0] = ('assign', p[1], p[3])


def p_statement_concat(p):
    'statement : expression SEMICOLON statement'
    p[0] = ('concatenate', p[1], p[3])


def p_statement_if(p):
    'statement : IF contents FI'
    p[0] = ('if', p[2])


def p_statement_do(p):
    'statement : DO contents OD'
    p[0] = ('do', p[2])


# 3. content

def p_content_guard(p):
    'content : expression ARROW expression'
    p[0] = ('guard', p[1], p[3])

def p_contents_one(p):
    '''contents : content'''
    p[0] = p[1]

def p_contents(p):
    'contents : content OR contents'
    p[0] = ('contents', p[1], p[3])


# 2. variables 와 expressions

def p_variables_one(p):
    '''variables : VARIABLE'''
    p[0] = p[1]

def p_variables(p):
    '''variables : VARIABLE COMMA variables'''
    p[0] = ("variables", p[1], p[3])

def p_expressions_one(p):
    '''expressions : expression'''
    p[0] = p[1]

def p_expressions(p):
    '''expressions : expression COMMA expressions'''
    p[0] = ("expressions", p[1], p[3])


# 1. expression 기능들

def p_expression(p):
	'''expression : expression PLUS expression
				| expression MINUS expression
				| expression TIMES expression
				| expression DIVIDE expression
	'''
	p[0] = (p[2], p[1], p[3])

def p_expression_one(p):
	'''expression : NUMBER 
				| VARIABLE'''
	p[0] = p[1]

def p_expression_paren(p):
	'''expression : LPAREN expression RPAREN'''
	p[0] = ("paren", p[2])



# Build the parser
parser = yacc.yacc(debug=1)

while True:
	try:
		s = input('GCL > ')
	except EOFError:
		break
	if not s: continue
	result = parser.parse(s, tracking=True, debug=1)
	print(result)

