
# Guarded Command Languages
* 2018. 6. 7
* CS522 형식언어 및 오토마타 
* 20183111 김이한

## 개요
* 2018 봄학기 형식언어 및 오토마타 이론 프로젝트 1 ~ 2
* Guarded Command Language(이하 GCL)의 파싱 및 실행 기능 구현

## Statement 문법 설명
### abort
* 논문에는 "do anything"이라고 하나, 사실상 의미가 없다고 보아
* 해당 시점에 프로그램을 중단하고 모든 변수 출력

### skip 
* 논문에는 "do nothing"이라 설명하고 있음
* 아무것도 하지 않음

### concatenation(;)
```
<statement>; <statement>[; <statement>]
```
* 여러 개의 statement가 연접할 수 있으며, 마지막 statement 뒤에는 세미콜론이 붙지 않음
* 두 개의 statement를 차례대로 실행

### assign(:=)
```
<variable>[; <variable>] := <expression>[; <expression>]
```
* 좌변에 있는 변수들을 우변에 있는 값으로 치환
* 우변에는 단순 숫자(number) 뿐만 아니라 사칙 / 논리 연산을 수반한 식을 사용할 수 있음
* 세미콜론으로 variable과 expression을 연접할 수 있음. 
  - 다만 좌변과 우변의 길이가 같은지는 파싱 단계에서 연산하지 않으며,
  - AST를 실행할 때 에러를 일으키게 됨

### selection (if ... fi)
* if 문의 문법은 다음과 같음
```
if    <guard> -> <statement>
   [| <guard> -> <statement>]
fi
```
* 모든 guard문을 실행하여 진위 여부를 파악
  - guard가 참인 statement 중 무작위로 하나를 실행하고 종료

### iteration (do ... od)
* if문의 문법과 동일 
```
do   <guard> -> <statement>
  [| <guard> -> <statement>]
od
```
* do문은 병렬로 연결된 guard문이 모두 거짓이 될 때까지 반복해서 실행
  - 각 실행 단계마다 모든 guard의 참/거짓을 계산
  - guard가 참인 statement 중 무작위로 하나를 실행하고 다음 실행 단계로 넘어감

## 사용법
* 하나의 프로그램은 한 줄로 이루어져 있음
* 

```console
kabi@DESKTOP-KJCD9CN:~$ git clone https://github.com/yihankim/cs522 ~/gcl
kabi@DESKTOP-KJCD9CN:~$ cd gcl
kabi@DESKTOP-KJCD9CN:~/gcl$ sudo apt-get install -y python3-pip
kabi@DESKTOP-KJCD9CN:~/gcl$ pip3 install ply
kabi@DESKTOP-KJCD9CN:~/gcl$ python3 main.py
GCL > a := 3; b := 5; m := a + b
{'b': 5, 'm': 8, 'a': 3}
GCL > x := 1; y := 10; do y > 0 -> x := x * 2; y := y - 1 od
{'y': 0, 'x': 1024}
GCL >
bye
kabi@DESKTOP-KJCD9CN:~/gcl$
```
