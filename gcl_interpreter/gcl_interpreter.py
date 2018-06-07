# CS522 프로젝트 #2
# 20130143 김이한

# 1. 개요
# yacc에서 생성된 AST를 실행하고 결과를 제출

# 2. 규칙
# AST head에 대응하는 규칙 실행
# variable : variable 테이블에서 값을 읽어 치환
# number : 값을 입력
# 연산자(+, -, ...) : ...

import random

#debug = True
debug = False

# soft print
def soft_print(level, *s):
    if debug:
        print('    ' * level, end='')
        print(s)

def eval_expr(expr, lookup_table = dict(), level = 0):
        soft_print(level, 'before evaluate', expr, lookup_table)
        level += 1

        # case 1: 숫자
        if expr[0] == "number":
            result = expr[1]

        # case 2: 변수
        if expr[0] == "variable":
            try:
                result = lookup_table[expr[1]]
            except KeyError:
                return None

        # case 3: not
        if expr[0] == "!":
            value = eval_expr(expr[1], lookup_table, level)
            result = int(not value)

        # case 4: binary boolean
        if expr[0] in ['&&', '||', '^', '==', '!=', '>', '<', '>=', '<=']:
            op = expr[0]
            v1 = eval_expr(expr[1], lookup_table, level)
            v2 = eval_expr(expr[2], lookup_table, level)
            table = {'&&': 'and', '||': 'or'}
            # expr[0]이 C 기호로 사용되어 python과 호환되지 않으므로 수정 필요
            if expr[0] in table.keys():
                op = table[expr[0]]
                v1 = bool(v1)
                v2 = bool(v2)
            
            result = int(eval("%s %s %s" % (v1, op, v2)))

        # case 5: binary arithmetic
        if expr[0] in ['+', '-', '*', '/']:
            op = expr[0]
            if op == "/":
                op = "//"
            v1 = eval_expr(expr[1], lookup_table, level)
            v2 = eval_expr(expr[2], lookup_table, level)
            result = eval("%s %s %s" % (v1, op, v2))

        # case 6: parenthesis
        if expr[0] == 'paren':
            result = eval_expr(expr[1], lookup_table, level)


        level -= 1
        try:
            soft_print(level, 'after evaluate', result, lookup_table)
            return result
        except:
            raise Exception('주어진 %s 토큰을 읽을 수 없습니다.' % expr)


def refine_content(contents):
    # contents = ['contents', ['guard', <E>, <S>], ['guard', <E>, <S>], ...]
    conds = list(map(lambda content: content[1], contents[1:]))
    clauses = list(map(lambda content: content[2], contents[1:]))
    return (conds, clauses)


def select_from_list(conds):
    # conds = [True|False]+
    assert any(conds)
    select = random.randint(0, len(conds) - 1) 
    while conds[select] == 0:
        select = random.randint(0, len(conds) - 1)
    return select


def eval_stmt(stmt, lookup_table = dict(), level = 0):
        soft_print(level, 'before execute', stmt, lookup_table)
        level += 1

        # do nothing
        if stmt[0] == 'skip':
            result = lookup_table

        # do anything: 실질적으로 구현 불가능하므로 예외 처리
        if stmt[0] == 'abort':
            print(lookup_table)
            raise Exception('abort 문이 실행되었습니다.')

        if stmt[0] == 'assign':
            variables = list(map(lambda var: var[1], stmt[1][1:]))
            values = stmt[2][1:]
            # AST 생성 단계에서 variables와 values의 길이를 비교할 수 있으나
            # 구현 상의 편이를 위해 실행 단에서 확인함
            if len(variables) != len(values):
                raise Exception('할당 시 변수와 값의 수가 일치하지 않습니다.')
            new_lookup_table = lookup_table.copy()
            for var, val in zip(variables, values):
                new_lookup_table[var] = eval_expr(val, lookup_table, level)
            result = new_lookup_table

        if stmt[0] == 'concat':
            for child_stmt in stmt[1:]:
                lookup_table = eval_stmt(child_stmt, lookup_table, level)
            result = lookup_table

        if stmt[0] == 'if':
            conds, clauses = refine_content(stmt[1])
            # 모든 cond를 실행하고 가능성 있는 element 선택
            eval_conds = list(map(lambda expr: eval_expr(expr, lookup_table, level), conds))
            if not any(eval_conds):
                raise Exception('if 문의 문장이 실행되지 않았습니다.')
            select = select_from_list(eval_conds)
            lookup_table = eval_stmt(clauses[select], lookup_table, level)
            result = lookup_table

        if stmt[0] == 'do':
            conds, clauses = refine_content(stmt[1])
            # 모든 cond를 실행하고 가능성 있는 element 선택
            eval_conds = list(map(lambda expr: eval_expr(expr, lookup_table, level), conds))
            while any(eval_conds):
                select = select_from_list(eval_conds)
                lookup_table = eval_stmt(clauses[select], lookup_table)
                eval_conds = list(map(lambda expr: eval_expr(expr, lookup_table, level), conds))
            result = lookup_table

        level -= 1
        try:
            soft_print(level, 'after execute', stmt, lookup_table)
            return result
        except:
            raise Exception("주어진 %s 토큰을 읽을 수 없습니다" % stmt[0])

