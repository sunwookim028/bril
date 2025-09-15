# forms basic blocks.

import json
import sys

if __name__ == '__main__':
	prog = json.load(sys.stdin)
	for func in prog['functions']:
		print(f"@{func['name']}")
		bb_id = 0
		was_jb = False
		first = True
		for instr in func['instrs']:
			if 'label' in instr or was_jb or first:
				print(f"bb #{bb_id}")
				bb_id = bb_id + 1
				if first:
					first = False
			print(instr)
			if 'label' not in instr and instr['op'] in {'jmp', 'br', 'ret'}:
				was_jb = True
			else:
				was_jb = False
		print("")
		print("")
