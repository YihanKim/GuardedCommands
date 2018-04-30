

import ply.yacc as yacc
from gcl_lex import tokens

# 1. expression_ 기능들
'''
expression_ 
<E> ::= <I>
	<V>
	<E> * <E>
	<E> / <E>
	<E> + <E>
	<E> - <E>
	(<E>)
'''

def p_expression__mult(p):
	'expression_ : expression_ TIMES expression_'
	p[0] = ('mult', p[1], p[3])

def p_expression__div(p):
	'expression_ : expression_ DIVIDE expression_'
	p[0] = ('div', p[1], p[3])

def p_expression__add(p):
	'expression_ : expression_ PLUS expression_'
	p[0] = ('add', p[1], p[3])

def p_expression__sub(p):
	'expression_ : expression_ MINUS expression_'
	p[0] = ('sub', p[1], p[3])

def p_expression__group(p):
	'expression_ : LPAREN expression_ RPAREN'
	p[0] = ('parenthesis', p[2])

def p_expression__number(p):
	'expression_ : NUMBER'
	p[0] = ('integer', p[1])

def p_expression__variable(p):
	'expression_ : VARIABLE'
	p[0] = ('variable', p[1])


# 2. variables 와 expressions
'''
variables 
<Vs> ::= <V>[,<V>]

expressions
<Es> ::= <E>[,<E>]
'''
def p_variables(p):
	'variables : VARIABLE variables_2'
	p[0] = ('variables', p[1], p[2])

def p_variables_terminate(p):
	'variables_2 : '
	p[0] = ('None')

def p_variables_loop(p):
	'variables_2 : COMMA VARIABLE variables_2'
	p[0] = ('variables', p[2], p[3])

def p_expressions(p):
    'expressions : expression_ expressions_2'
    p[0] = ('variables', p[1], p[2])

def p_expressions_terminate(p):
	'expressions_2 : '
	p[0] = ('None')

def p_expressions_loop(p):
	'expressions_2 : COMMA expression_ expressions_2'
	p[0] = ('expressions', p[2], p[3])

# 3. content
'''
content 
<C> ::= <E> -> <S>
'''

def p_content_guard(p):
	'content : expression_ ARROW statement'
	p[0] = ('guard', p[1], p[3])

def p_contents(p):
	'contents : content contents_2'
	p[0] = ('contents', p[1], p[2])

def p_contents_terminate(p):
	'contents_2 : '
	p[0] = ('None')

def p_contents_loop(p):
	'contents_2 : OR content contents_2'
	p[0] = ('contents', p[2], p[3])


# 4. statement

def p_statement_skip(p):
	'statement : SKIP'
	p[0] = ('skip')

def p_statement_abort(p):
	'statement : ABORT'
	p[0] = ('abort')

def p_statement_assign(p):
	'statement : variables ASSIGN expressions'
	p[0] = ('assign', p[1], p[3])

def p_statement_concat(p):
	'statement : expression_ SEMICOLON statement'
	p[0] = ('concatenate', p[1], p[3])

def p_statement_if(p):
	'statement : IF contents FI'
	p[0] = ('if', p[1])

def p_statement_do(p):
	'statement : DO contents OD'
	p[0] = ('do', p[1])


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

