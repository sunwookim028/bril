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
  new_block = []
  # Handle label and terminators.
  if 'label' in block[0]:
    new_block.append(block[0])
    block = block[1:]
  term = None
  if (block and block[-1] and
      block[-1]['op'] in TERMINATORS):
    term = block[-1]
    block = block[:-1]
  # Key data structures.
  # prev_rhs and canonical_vars share indices, 
  # which are values of the lvn mapping.
  var_to_lvn = dict()
  prev_rhs = [] # if binary op, always lvn1<lvn2.
  canonical_vars = []
  # Main loop
  for instr in block:
    if 'dest' not in instr:
      # transform only
      if "args" in instr:
        new_args = []
        for arg in instr["args"]:
          if arg not in var_to_lvn:
            var_to_lvn[arg] = len(prev_rhs)
            prev_rhs.append(None)
            canonical_vars.append(None)
          lvn = var_to_lvn[arg]
          if canonical_vars[lvn] != None:
            new_args.append(canonical_vars[lvn])
          else:
            new_args.append(arg)
        instr["args"] = new_args
      new_block.append(instr)
      continue
    # Core logic.
    # 1/2, Find match in the canonical tuple form.
    if instr['op'] == 'const':
      rhs_in_lvn = ('const', instr['value'])
    else:
      args_in_lvn = []
      for arg in instr['args']:
        # handle args from other blocks above
        if arg not in var_to_lvn.keys():
          next_lvn = len(prev_rhs)
          var_to_lvn[arg] = next_lvn
          prev_rhs.append(None)
          canonical_vars.append(None)
        args_in_lvn.append(var_to_lvn[arg])
      args_in_lvn.sort()
      if 'funcs' in instr:
        rhs_in_lvn = ['call', instr['funcs']]
      else:
        rhs_in_lvn = [instr['op']]
      if args_in_lvn:
        rhs_in_lvn = rhs_in_lvn + args_in_lvn
      rhs_in_lvn = tuple(rhs_in_lvn)
    hit = False
    i = 0
    for some_prev_rhs in prev_rhs:
      if rhs_in_lvn == some_prev_rhs:
        hit = True
        break
      i = i + 1
    # 2/2, update the 3 data structures
    # and append instr in the correct form.
    var_to_lvn[instr['dest']] = i
    if hit:
      # prev_rhs and canonical_vars don't update.
      instr["op"] = "id"
      instr["args"] = [canonical_vars[i]]
    else:
      prev_rhs.append(rhs_in_lvn)
      canonical_vars.append(instr["dest"])
      if "args" in instr:
        new_args = []
        for arg in instr["args"]:
          lvn = var_to_lvn[arg]
          if canonical_vars[lvn] != None:
            new_args.append(canonical_vars[lvn])
          else:
            new_args.append(arg)
        instr["args"] = new_args
    new_block.append(instr)
  if term:
    new_block.append(term)
  return new_block


def lvn_pass(func):
  """Returns the transformed version of the input
     function, where (some) common subexpressions
     from each basic block are eliminated.
  """
  from bb import form_blocks
  new_instrs = []
  for block in form_blocks(func):
    new_instrs = new_instrs + eliminate_common(block)
  func['instrs'] = new_instrs
  return func
    

if __name__ == "__main__":
  from briltxt import print_func
  bril = json.load(sys.stdin)
  for func in bril['functions']:
    print_func(lvn_pass(func))
