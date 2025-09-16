"""Form basic blocks from each function in a Brill program.
"""

import json
import sys


TERMINATORS = {'jmp', 'br', 'ret'}


def form_blocks(func):
  """Returns a list of basic blocks from the function,
  where each block is a list of instructions.
  """
  cur_block = []
  for instr in func['instrs']:
    if 'label' in instr:
      if cur_block:
        yield cur_block
        cur_block = []
    cur_block.append(instr)
    if 'label' not in instr and instr['op'] in TERMINATORS:
      yield cur_block
      cur_block = []
  if cur_block:
    yield cur_block


def print_blocks(func):
  """Prints out the block to stdout.
  """
  import briltxt
  for i, block in enumerate(form_blocks(func)):
    # print out block header
    if 'label' in block[0]:
      print(f"{func['name']}.block{i} ({block[0]['label']}):")
      block = block[1:]
    else:
      print(f"{func['name']}.block{i}:")
    for instr in block:
      # indent then print the json instr in a txt form.
      print("  {}".format(briltxt.instr_to_string(instr)))


if __name__ == '__main__':
  bril = json.load(sys.stdin)
  for func in bril['functions']:
    print_blocks(func)
