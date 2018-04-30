
import ply.yacc as yacc
from gcl_lex import tokens




# 1. expression 기능들

def p_expression(p):
	'''expressio : expressio PLUS expressio
				| expressio MINUS expressio
				| expressio TIMES expressio
				| expressio DIVIDE expressio
	'''

def p_expression_one(p):
	'''expressio : NUMBER 
				| VARIABLE'''
	p[0] = p[1]

def p_expression_paren(p):
	'''expressio : LPAREN expressio RPAREN'''
	p[0] = ("paren", p[2])


# 2. variables 와 expressions

def p_variables_one(p):
	'''variables : VARIABLE'''
	p[0] = p[1]

def p_variables(p):
	'''variables : VARIABLE COMMA variables'''
	p[0] = ("variables", p[1], p[3])

def p_expressions_one(p):
	'''expressions : expressio'''
	p[0] = p[1]

def p_expressions(p):
	'''expressions : expressio COMMA expressions'''
	p[0] = ("expressions", p[1], p[3])


# 3. content

def p_content_guard(p):
	'content : expressio ARROW statement'
	p[0] = ('guard', p[1], p[3])

def p_contents_one(p):
	'''contents : content'''
	p[0] = p[1]

def p_contents(p):
	'contents : content OR contents'
	p[0] = ('contents', p[1], p[3])


# 4. statement

def p_statement_one(p):
	'''statement : SKIP
				| ABORT'''
	p[0] = p[1]


def p_statement_assign(p):
	'statement : variables ASSIGN expressions'
	p[0] = ('assign', p[1], p[3])


def p_statement_concat(p):
	'statement : expressio SEMICOLON statement'
	p[0] = ('concatenate', p[1], p[3])


def p_statement_if(p):
	'statement : IF content FI'
	p[0] = ('if', p[2])


def p_statement_do(p):
	'statement : DO content OD'
	p[0] = ('do', p[2])


# Error rule for syntax errors
def p_error(p):
	print("Syntax error in input!")


# Build the parser
parser = yacc.yacc(debug=1)

while True:
	try:
		s = input('calc > ')
	except EOFError:
		break
	if not s: continue
	result = parser.parse(s, tracking=True, debug=1)
	print(result)

