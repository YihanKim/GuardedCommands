
# Guarded Command Language parser
2018 봄학기 CS522 형식언어 및 오토마타 이론 프로젝트 1
20183111 김이한

## 개요
* lex와 yacc을 이용한 파서로 AST 트리 생성하기
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
	| <Vs> := <Es>
	| <Ss>
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

Statements
<Ss> ::= <S>[,<S>]

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

$ python3 gcl_yacc.py

GCL > if x * 3 + 1 -> y fi
('if', ('guard', ('+', ('*', 'x', 3), 1), 'y'))

GCL > thisismyvariablewhichislongerthantheotherexample := 10000000000000000000000000000
('assign', 'thisismyvariablewhichislongerthantheotherexample', 10000000000000000000000000000)

GCL > do x->y | y->z | z->x od
('do', ('contents', ('guard', 'x', 'y'), ('contents', ('guard', 'y', 'z'), ('guard', 'z', 'x'))))

GCL > ^Z

$ python3 main.py input.txt

['abort']

['skip']

['assign', ['variables', 'v'], ['expressions', 1]]

['assign', ['variables', 'a', 'b'], ['expressions', 2, 3]]

['assign',
 ['variables', 'ash', 'ben', 'carl', 'dave'],
 ['expressions', 12893892189, 4848, 85912389548932, 1]]

['assign',
 ['variables', 't', 'u', 'v'],
 ['expressions', ['paren', ['+', 3, ['/', 5, 7]]], ['-', 8, 3], 6]]

['concat',
 ['assign', ['variables', 'x'], ['expressions', 1]],
 ['assign', ['variables', 'y'], ['expressions', 2]]]

['concat',
 ['concat',
  ['concat',
   ['assign', ['variables', 'x'], ['expressions', 3]],
   ['assign', ['variables', 'y'], ['expressions', 4]]],
  ['assign', ['variables', 'z'], ['expressions', ['+', 'x', 'y']]]],
 ['abort']]

['abort']

['if',
 ['guard',
  ['-', 'x', 'y'],
  ['assign', ['variables', 'y'], ['expressions', 'x']]]]

['if',
 ['contents',
  ['guard',
   ['+', 'x', 'y'],
   ['assign', ['variables', 'z'], ['expressions', ['+', 'z', 3]]]],
  ['guard',
   ['+', 'y', 'z'],
   ['assign', ['variables', 'x'], ['expressions', ['+', 'x', 3]]]],
  ['guard',
   ['+', 'z', 'x'],
   ['assign', ['variables', 'y'], ['expressions', ['+', 'y', 3]]]]]]

['skip']

['do',
 ['contents',
  ['guard',
   ['+', 'x', 'y'],
   ['assign', ['variables', 'z'], ['expressions', ['+', 'z', 3]]]],
  ['guard',
   ['+', 'y', 'z'],
   ['assign', ['variables', 'x'], ['expressions', ['+', 'x', 3]]]],
  ['guard',
   ['+', 'z', 'x'],
   ['assign', ['variables', 'y'], ['expressions', ['+', 'y', 3]]]]]]

['concat',
 ['assign', ['variables', 'a', 'b'], ['expressions', 'A', 'B']],
 ['do',
  ['contents',
   ['guard',
    ['-', 'b', 'a'],
    ['assign', ['variables', 'b'], ['expressions', ['-', 'b', 'a']]]],
   ['guard',
    ['-', 'a', 'b'],
    ['assign', ['variables', 'a'], ['expressions', ['-', 'a', 'b']]]]]]]

['concat',
 ['assign',
  ['variables', 'a', 'b', 'x', 'y', 'u', 'v'],
  ['expressions', 'A', 'B', 1, 0, 0, 1]],
 ['do',
  ['guard',
   'b',
   ['concat',
    ['assign',
     ['variables', 'q', 'r'],
     ['expressions',
      ['/', 'a', 'b'],
      ['-', 'a', ['*', ['paren', ['/', 'a', 'b']], 'b']]]],
    ['assign',
     ['variables', 'a', 'b', 'x', 'y', 'u', 'v'],
     ['expressions',
      'b',
      'r',
      'u',
      'v',
      ['-', 'x', ['*', 'q', 'u']],
      ['-', 'y', ['*', 'q', 'v']]]]]]]]

$
```
