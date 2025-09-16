"""Prints out the transformed version of input Bril
   program, where (some) common subexpressions are 
   eliminated.
"""

import sys
import json

from bb import TERMINATORS


def eliminate_common(block):
  """Returns the transformed version of the input
     basic block, where (some) common subexprs are 
     eliminated.
  """
  if 'label' in block[0]:
    yield block[0]
    block = block[1:]
  term = ""
  if (block and block[-1] and
      block[-1]['op'] in TERMINATORS):
    term = block[-1]
    block = block[:-1]
  for instr in block:
    yield instr
  if term:
    yield term


def lvn_pass(func):
  """Returns the transformed version of the input
     function, where (some) common subexpressions
     from each basic block are eliminated.
  """
  from bb import form_blocks
  new_instrs = []
  for block in form_blocks(func):
    new_block = eliminate_common(block)
    for instr in new_block:
      new_instrs.append(instr)
  func['instrs'] = new_instrs
  return func
    

if __name__ == "__main__":
  from briltxt import print_func
  bril = json.load(sys.stdin)
  for func in bril['functions']:
    print_func(lvn_pass(func))
