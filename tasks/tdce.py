""" Trivial dead code elimination.
"""

import json
import sys
from bb import TERMINATORS

SIDE_EFFECT = {'print', 'call'}


def eliminate(block):
  """ Given a basic block, a list of Bril instructions,
  eliminate trivially dead instructions, i.e. assignments
  that are overwritten before referred.
  """
  to_delete = set()
  yet_unused = {}
  for i, instr in enumerate(block):
    # referenced instr gets alive 
    if 'args' in instr:
      for var in instr['args']:
        if var in yet_unused:
          del yet_unused[var]
    if 'label' in instr: continue
    if instr['op'] in TERMINATORS: continue
    if instr['op'] in SIDE_EFFECT: continue
    if instr['op'] == 'nop':  
      to_delete.add(i)
      continue
    # all instrs that come here has a dest variable.
    dest = instr['dest']
    # overwritten instr is dead
    if dest in yet_unused:
      to_delete.add(yet_unused[dest])
    yet_unused[dest] = i
  for i, instr in enumerate(block):
    if i not in to_delete:
      yield instr


if __name__ == '__main__':
  from bb import form_blocks
  from briltxt import print_func
  bril = json.load(sys.stdin)
  for func in bril['functions']:
    changed = True
    while changed:
      live_instrs = []
      orig_instr_cnt = len(func['instrs'])
      for block in form_blocks(func):
        live_instrs += eliminate(block)
        func['instrs'] = live_instrs
      new_instr_cnt = len(func['instrs'])
      changed = new_instr_cnt < orig_instr_cnt
    print_func(func)
