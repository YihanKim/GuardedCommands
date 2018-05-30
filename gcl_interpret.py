# CS522 프로젝트 #2
# 20130143 김이한

# 1. 개요
# yacc에서 생성된 AST를 실행하고 결과를 제출

# 2. 규칙
# AST head를 읽고 작동
# variable : variable 테이블에서 값을 읽어 치환
# number : 값을 입력
# 연산자(+, -, ...) : ...

def eval_expr(expr, lookup_table = dict()):
	try:
		# case 1: 숫자
		if expr[0] == "number":
			return expr[1]

		# case 2: 변수
		if expr[0] == "variable":

			try:
				return lookup_table[expr[1]]
			except KeyError:
				return None
	
		# case 3: not
		if expr[0] == "!":
			value = eval_expr(expr[1], lookup_table)
			if value == 0:
				return 0
			else:
				return 1

		# case 4: and, not, xor
		if expr[0] in ['and', 'or', 'xor']:
			v1 = eval_expr(expr[1], lookup_table)
			v2 = eval_expr(expr[2], lookup_table)
			
		else:
			
	except:
		return None


