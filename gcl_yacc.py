
import ply.yacc as yacc
from gcl_lex import tokens

# group은 우선순위 의미

precedence = (
                # 우선순위 낮음
		('nonassoc', 'IF', 'FI', 'DO', 'OD'),
		('left', 'SEMICOLON'),
		('nonassoc', 'ARROW', 'ASSIGN'),
		('left', 'COMMA'),
                ('left', 'OR'), # group 14
                ('left', 'XOR'), # group 11
                ('left', 'AND'), # group 10
                ('left', 'EQUAL', 'NOTEQUAL'), # group 9
                ('left', 'LESS', 'GREATER', 'LEQUAL', 'GEQUAL'), # group 8
		('left', 'PLUS', 'MINUS'), # group 6
		('left', 'TIMES', 'DIVIDE'), # group 5
                ('right', 'NOT'), # group 3
                # 우선순위 높음
)

# parser rule은 top-down으로 작성

# 4. statement

def p_statement_one(p):
    '''statement : SKIP
                | ABORT '''
    p[0] = (p[1],)

def p_statement_assign(p):
    'statement : variables ASSIGN expressions'
    p[0] = ('assign', p[1], p[3])

def p_statement_empty_if(p):
	'statement : IF FI'
	p[0] = ('abort',)

def p_statement_empty_do(p):
	'statement : DO OD'
	p[0] = ('skip',)

def p_statement_if(p):
    'statement : IF contents FI'
    p[0] = ('if', p[2])

def p_statement_do(p):
    'statement : DO contents OD'
    p[0] = ('do', p[2])

def p_statement_statements(p):
	'statement : statements'
	p[0] = p[1]

def p_statements_concat(p):
	#'''statement : statement SEMICOLON statement'''
	'''statements : statement SEMICOLON statement'''
	p[0] = ('concat', p[1], p[3])

# 3. content

def p_content_guard(p):
    'content : expression ARROW statement'
    p[0] = ('guard', p[1], p[3])

def p_contents_one(p):
    '''contents : content'''
    p[0] = p[1]

def p_contents(p):
    'contents : content SPLIT contents'
    p[0] = ('contents', p[1], p[3])


# 2. variables 와 expressions

def p_variables_one(p):
    '''variables : VARIABLE'''
    p[0] = ('variables', p[1])

def p_variables(p):
    '''variables : VARIABLE COMMA variables'''
    p[0] = ("variables", p[1], p[3])

def p_expressions_one(p):
    '''expressions : expression'''
    p[0] = ('expressions', p[1])

def p_expressions(p):
    '''expressions : expression COMMA expressions'''
    p[0] = ("expressions", p[1], p[3])


# 1. expression 기능들

def p_expression_binary(p):
	'''expression : expression PLUS expression
				| expression MINUS expression
				| expression TIMES expression
                                | expression DIVIDE expression
				| expression AND expression
				| expression OR expression
				| expression XOR expression
				| expression EQUAL expression
				| expression NOTEQUAL expression
				| expression LESS expression
				| expression GREATER expression
				| expression LEQUAL expression
				| expression GEQUAL expression
	'''
	p[0] = (p[2], p[1], p[3])

def p_expression_unary(p):
	'''expression : NOT expression'''
	p[0] = (p[1], p[2])

def p_expression_value(p):
	'''expression : NUMBER 
				| VARIABLE'''
	p[0] = p[1]

def p_expression_paren(p):
	'''expression : LPAREN expression RPAREN'''
	p[0] = ("paren", p[2])

def p_error(t):
    print("Syntax error at '%s'" % t.value)


# pretifier
import pprint

def prettify(s):
	if not type(s) == tuple:
		return s
	token = s[0]
	
	if s[0] in ('contents', 'expressions', 'variables', 'statements'):
		# 임시 변수 d를 사용하여 연결 리스트와 같이 되풀이하는 구조를 배열로 만들기
		d = s
		L = [d[0]]
		while True:
			L.append(prettify(d[1]))
			if len(d) == 2:
				break
			tmp = prettify(d[2])
			if type(tmp) == list and tmp[0] == s[0] and len(d) == 3:
				d = d[2]
				continue
			else:
				L.append(tmp)
				break
		return L
	
	else:
		return list(map(prettify, s))

# Build the parser
parser = yacc.yacc()

if __name__ == "__main__":
	while True:
		try:
			s = input('GCL > ')
		except EOFError:
			break
		if not s: 
			break
			continue
		result = parser.parse(s)
		pprint.pprint(prettify(result))

