from gcl_yacc import parser, prettify
from pprint import pprint, pformat
import sys

#print(parser)

def main():
    data = sys.argv

    if len(data) < 2:
        while True:
            try:
                s = input("GCL > ") 
            except:
                break
            if not s: 
                print("bye")	
                break

            result = parser.parse(s)
            try:
                pprint(prettify(result))
            except:
                print("failed to parse")

    elif len(data) <= 3:
        lines = [line.rstrip('\n') for line in open(data[1])]

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
                    result = parser.parse(line)
                    try:
                        d = prettify(result)
                        pprint(d)
                        f.write(str(d))
                    except:
                        print("failed to parse " + line)

                f.write('\n')

    else:
        print("use at most 2 arguments")

if __name__ == "__main__":
    main()
