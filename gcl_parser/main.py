from gcl_yacc import parser, prettify
from pprint import pprint, pformat
import sys

def safe_parse(s, print_result=False):
    try:
        result = parser.parse(s)
        result = prettify(result)
    except:
        print("파싱에 실패했습니다")
        return None

    if print_result:
        pprint(result)
    
    return result


def main():
    data = sys.argv

    if len(data) < 2:
        
        while True:
            try:
                s = input("GCL > ") 
            except KeyboardInterrupt:
                print()
                print("bye")
                break
            
            if not s: 
                print("bye")	
                break

            result = safe_parse(s, print_result = True)

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
                    result = safe_parse(line, print_result = True)
                    f.write('# ' + line + '\n')
                    f.write(str(result))

                f.write('\n')

    else:
        print("최대 2개의 인자만 사용 가능합니다.")

if __name__ == "__main__":
    main()
