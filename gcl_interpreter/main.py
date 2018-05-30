from gcl_interpreter import eval_stmt, eval_expr
import sys


def safe_eval_stmt(s):
    try:
        result = eval_stmt(s, dict())
        return result
    except:
        print(sys.exc_info())
        return str()


def main():
    data = sys.argv

    if len(data) < 2:

        while True:
            try:
                s = input("AST > ")
            except KeyboardInterrupt:
                print()
                print("bye")
                break

            if not s:
                print("bye")
                break

            result = safe_eval_stmt(eval(s))

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
                    result = safe_eval_stmt(eval(line))
                    f.write(str(result))

                f.write('\n')


if __name__ == "__main__":
    main()
