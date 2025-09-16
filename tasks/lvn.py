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
  # Handle label and terminators.
  if 'label' in block[0]:
    yield block[0]
    block = block[1:]
  term = ""
  if (block and block[-1] and
      block[-1]['op'] in TERMINATORS):
    term = block[-1]
    block = block[:-1]
  # Key data structures.
  # prev_rhs and canonical_vars share indices, 
  # which are values of the lvn mapping.
  var_to_lvn = {}
  prev_rhs = [] # if binary op, always lvn1<lvn2.
  canonical_vars = []
  # Main loop
  for instr in block:
    if 'dest' not in instr:
      yield instr
    # Core logic.
    # 1/2, Find match in the canonical tuple form.
    hit = False
    for i, some_prev_rhs in enumerate(prev_rhs):
      # of the rhs of this instruction, which is
      # a constant or a value operation.
      if instr['op'] == 'const':
        rhs_in_lvn = () #FIXME
      else:
        rhs_in_lvn = () #FIXME
      if rhs_in_lvn == some_prev_rhs:
        hit = True
        break
    # 2/2, yield instr in the correct form
    # and update the 3 data structures.
    if hit: # Matched
      # TODO. update the 3 data structures
      # index is i.
      yield instr # FIXME. yield transformed instr
    else:
      # TODO. update the 3 data structures
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
