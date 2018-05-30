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
            return not value

        # case 4: binary boolean
        if expr[0] in ['&&', '||', '^', '==', '!=', '>', '<', '>=', '<=']:
            op = expr[0]
            table = {'&&': 'and', '||': 'or', '^': 'xor'}
            # expr[0]이 C 기호로 사용되어 python과 호환되지 않으므로 수정 필요
            if expr[0] in ['and', 'or', 'xor']:
                op = table[expr[0]]

            v1 = bool(eval_expr(expr[1], lookup_table))
            v2 = bool(eval_expr(expr[2], lookup_table))
            return eval("%s %s %s" % (v1, op, v2))
        
        # case 5: binary arithmetic
        if expr[0] in ['+', '-', '*', '/']:
            v1 = eval_expr(expr[1], lookup_table)
            v2 = eval_expr(expr[2], lookup_table)
            return eval("%s %s %s" % (v1, expr[0], v2))

        # case 6: parenthesis
        if expr[0] == 'paren':
            return eval(eval_expr(expr[1], lookup_table))

        else:
            raise Exception('주어진 %s 토큰을 읽을 수 없습니다.' % expr[0])

    except:
        raise Exception('%s 실행 중 오류가 발생했습니다.' % expr)


def refine_content(contents):
    # contents = ['contents', ['guard', <E>, <S>], ['guard', <E>, <S>], ...]
    conds = list(map(lambda content: content[1], contents[1:]))
    clauses = list(map(lambda content: content[2], contents[1:]))
    return (conds, clauses)


def select_from_list(conds):
    # conds = [True|False]+
    assert any(conds)

    select = random.randint(0, len(conds) - 1) 
    while not conds[select]:
        select = random.randint(0, len(conds) - 1)

    return select


def eval_stmt(stmt, lookup_table = dict()):
    try:
        # do nothing
        if stmt[0] == 'skip':
            return lookup_table

        # do anything: 실질적으로 구현 불가능하므로 예외 처리
        if stmt[0] == 'abort':
            print(lookup_table)
            raise Exception('abort 문이 실행되었습니다.')

        if stmt[0] == 'assign':
            variables = stmt[1][1:]
            values = stmt[2][1:]
            # AST 생성 단계에서 variables와 values의 길이를 비교할 수 있으나
            # 구현 상의 편이를 위해 실행 단에서 확인함
            if len(variables) != len(values):
                raise Exception('할당 시 변수와 값의 수가 일치하지 않습니다.')
            for var, val in zip(variables, values):
                lookup_table[var] = eval_expr(val, lookup_table)
            return lookup_table

        if stmt[0] == 'concat':
            for child_stmt in stmt[1:]:
                lookup_table = eval_stmt(child_stmt, lookup_table)
            return lookup_table
        
        if stmt[0] == 'if':
            conds, clauses = refine_content(stmt[1])
            # 모든 cond를 실행하고 가능성 있는 element 선택
            eval_conds = list(map(lambda expr: bool(eval_expr(expr, lookup_table)), conds))
            if not any(eval_conds):
                print(lookup_table)
                raise Exception('if 문의 문장이 실행되지 않았습니다.')
            
            select = select_from_list(conds)
            lookup_table = eval_stmt(clauses[stmt])
            return lookup_table
            
        if stmt[0] == 'do':
            conds, clauses = refine_content(stmt[1])
            # 모든 cond를 실행하고 가능성 있는 element 선택
            eval_conds = list(map(lambda expr: bool(eval_expr(expr, lookup_table)), conds))
            while any(eval_conds):
                select = select_from_list(conds)
                lookup_table = eval_stmt(clauses[stmt])
            return lookup_table
    except:
        raise Exception("%s Statement 실행 중 오류가 발생했습니다." % stmt)

def main():
    while True:
        print(eval_stmt(eval(input())))


if __name__ == "__main__":
    main()
