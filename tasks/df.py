"""Dataflow framework defined variables analyzer
"""


def definitions(blocks, block_idx, cfg, func_args):
  """Returns the set of defined vars in bb{block_idx}.
  """
  return {instr['dest'] for instr in blocks[block_idx] if 'dest' in instr}


def defined_out(blocks, block_idx, cfg, func_args):
  """OUT func for defined_vars analysis.

     Returns the set of defined vars at the exit of bb{block_idx}.
  """
  defined_vars = defined_in(block_idx, cfg, func_args)
  defined_vars.update(definitions(blocks, block_idx, cfg, func_args))
  return defined_vars


def defined_in(block_idx, cfg, func_args):
  """IN func for defined_vars analysis.

     Returns the set of defined vars at the entry of bb{block_idx}.
  """
  if block_idx == 0:
    return set() #FIXME just to test against the ref impl
    #return set(func_args)
  defined_vars = set()
  for u, v in cfg:
    if v == block_idx:
      defined_vars.update(defined_out(blocks, u, cfg, func_args))
  return defined_vars


def df_defined_vars(cfg, func_args, blocks): #FIXME count |V| from cfg
  """Top-level function for driving defined_vars analysis.

     Runs the worklist algorithm then prints out names 
     of every variables that are defined when each block is
     entered. Currently types are not being checked.

     This func assumes that the caller guarantees that bb0 is the entry block.
  """
  func_arg_names = [arg['name'] for arg in func_args]
  # Run worklist algorithm
  worklist = set(range(len(blocks)))
  work_in = [None for _ in range(len(blocks))]
  work_out = [None for _ in range(len(blocks))]
  while worklist:
    work_block_idx = worklist.pop()
    work_in[work_block_idx] = defined_in(work_block_idx, cfg, func_arg_names)
    work_block_out = defined_out(blocks, work_block_idx, cfg, func_arg_names)
    if work_block_out != work_out[work_block_idx]:
      work_out[work_block_idx] = work_block_out
      for u, v in cfg:
        if u == work_block_idx:
          worklist.add(v)
  # Print results
  for block_idx in range(len(blocks)):
    print(f"bb{block_idx}:") #FIXME pass and print block labels instead
    if not work_in[block_idx]:
      print(f"  in:  ∅")
    else:
      print(f"  in:  {', '.join(sorted(list(work_in[block_idx])))}")
    if not work_out[block_idx]:
      print(f"  out: ∅")
    else:
      print(f"  out: {', '.join(sorted(list(work_out[block_idx])))}")


if __name__ == '__main__':
  import json
  import sys
  from cfg import form_blocks, form_cfg
  prog = json.load(sys.stdin)
  for func in prog['functions']:
    blocks = list(form_blocks(func['instrs']))
    cfg = list(form_cfg(blocks))
    func_args = func.get('args', []) #AI-generated simpler syntax
    df_defined_vars(cfg, func_args, blocks)
