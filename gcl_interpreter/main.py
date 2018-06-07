from gcl_interpreter import eval_stmt, eval_expr
import sys
sys.path.append('../gcl_parser')
from gcl_yacc import parser, prettify

def safe_eval_stmt(s):
    try:
        result = eval_stmt(s, dict())
        return result
    except Exception as e:
        return e

def main():
    data = sys.argv

    if len(data) < 2:
        mode = input("사용할 모드를 입력하세요(GCL / AST) : ")
		
        while mode not in ['GCL', 'AST']:
            if not mode or mode == 'exit':
                print('bye')
                return
            mode = input("사용할 모드를 입력하세요(GCL / AST) : ")

        while True:
            try:
                s = input("%s > " % mode)
            except KeyboardInterrupt:
                print("bye")
                break

            if not s:
                print("bye")
                break

            if mode == "GCL":
                try:
                    s = prettify(parser.parse(s))
                except:
                    print("파싱 과정 중 오류가 발생했습니다.")
            if mode == "AST":
                try:
                    s = eval(s)
                except:
                    print("AST를 읽을 수 없습니다.")
            try:
                result = safe_eval_stmt(s)
                print(result)
            except Exception as e:
                print("실행 중 오류 : %s" % e)

    elif len(data) <= 3:
        try:
            with open(data[1], 'r') as f:
                lines = [line.rstrip('\n') for line in f]
        except:
            print("파일을 여는 데 실패했습니다.")
            return

        # 파일 이름 : 두 번째 인자가 없을 경우 output.txt 생성 후 저장
        if len(data) == 2:
            output_file = 'output.txt'
        else:
            output_file = data[2]

        with open(output_file, 'w') as f:
            for line in lines:
                if len(line) == 0:
                    print(line)
                elif line[0] == "#":
                    print(line)
                    f.write(line)
                else:
                    #print(line)
                    result = safe_eval_stmt(eval(line))
                    print(result)
                    f.write(str(result))

                f.write('\n')


if __name__ == "__main__":
    main()
