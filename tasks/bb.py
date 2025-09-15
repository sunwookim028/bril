"""Form basic blocks from each function in a Brill program.
"""

import json
import sys


def form_blocks(func):
  """Returns a list of basic blocks from the function,
  where each block is a list of instructions.
  """
  #FIXME!!
  #unit test. return 1 block allways.
  cur_block = []
  for instr in func['instrs']:
    cur_block.append(instr)
  if cur_block:
    yield cur_block


if __name__ == '__main__':
  import briltxt
  bril = json.load(sys.stdin)
  for func in bril['functions']:
    blocks = form_blocks(func)
    for i, block in enumerate(blocks):
      if 'label' in block[0]:
        print(f"{func['name']}.block{i} ({block[0]['label']}):")
        block = block[1:]
      else:
        print(f"{func['name']}.block{i}:")
      for instr in block:
        # indent then print the json instr in a txt form.
        print("  {}".format(briltxt.instr_to_string(instr)))
    '''
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
    '''
