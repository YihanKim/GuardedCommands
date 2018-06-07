
# CS522 프로젝트 제출물 #2
# 20183111 김이한

import sys
sys.path.insert(0, './gcl_parser')
from gcl_parser import main as gcl_parse_main
sys.path.insert(0, './gcl_interpreter')
from main import main as gcl_interpret_main

gcl_interpret_main()

