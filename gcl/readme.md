
# Guarded Command Language parser
20130143 김이한, CS522 형식언어 및 오토마타 이론 프로젝트 1

## 개요
* lex와 yacc을 이용한 파서 생성하기
* 사용 환경 : Linux, Python 3.5
* 사용 라이브러리 : PLY(Python Lex-Yacc)
* expression은 실행 결과를 값으로 표시 가능한 식을 대상으로 함
* statement는 guarded command의 기본 문법 단위

## 실행 방법(Ubuntu 16.04)
```
sudo apt-get install python3-pip
pip3 install ply
python3 gcl_yacc.py

```


## 문법 구조

```
statement 
<S> ::= skip
	| abort
	| <E>
	| <Vs> := <Es>
	| <S>;<S>
	| if <Cs> fi
	| do <Cs> od

variable <V> 
string except reserved letter (if, fi, do, od, skip, abort)

expression 
<E> ::= <I>
	| <V>
	| <E> * <E>
	| <E> / <E>
	| <E> + <E>
	| <E> - <E>
	| (<E>)

integer <I> 
string starts with consequent digits

variables 
<Vs> ::= <V>[,<V>]

expressions
<Es> ::= <E>[,<E>]

contents
<Cs> ::= <C>[|<C>]

content 
<C> ::= <E> -> <S>

```

## 실행 예시
```
$ GCL > if x * 3 + 1 -> y fi
('if', ('guard', ('+', ('*', 'x', 3), 1), 'y'))

$ GCL > thisismyvariablewhichislongerthantheotherexample := 10000000000000000000000000000
('assign', 'thisismyvariablewhichislongerthantheotherexample', 10000000000000000000000000000)

$ GCL > do x->y | y->z | z->x od
('do', ('contents', ('guard', 'x', 'y'), ('contents', ('guard', 'y', 'z'), ('guard', 'z', 'x'))))
```
