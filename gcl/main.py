from gcl_yacc import parser, prettify
from pprint import pprint, pformat
import sys

#print(parser)

if __name__ == "__main__":
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

	elif len(data) == 2:
		lines = [line.rstrip('\n') for line in open(data[1])]
		with open('output.txt', 'w') as f:
			for line in lines:
				if len(line) and line[0] != "#":
					result = parser.parse(line)
					try:
						d = prettify(result)
						pprint(d)
						f.write(str(pformat(d)))
						f.write('\n\n')
						print()
					except:
						print("failed to parse " + line)
	else:
		print("use only one argument")
